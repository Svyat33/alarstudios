import logging

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from data.notifier import publish

logger = logging.getLogger(__name__)


class DotsOrderedManyToManyField(models.ManyToManyField):
    def value_from_object(self, object):
        relation = getattr(object, self.attname)
        query = {self.related.var_name: object}
        qs = relation.through.objects.filter(**query).order_by('id')
        return Dot.objects.filter(pk__in=qs.values_list('dot_id', flat=True))


class Dot(models.Model):
    coord = models.PointField()
    name = models.CharField(max_length=200)

    def __repr__(self):
        return f"{self.name} {self.coord.x},{self.coord.y}"


class Track(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dots = DotsOrderedManyToManyField(Dot)
    length = models.IntegerField(default=0)

    @property
    def begin(self):
        return self.dots.all().first()

    @property
    def end(self):
        return self.dots.all().last()

    def __repr__(self):
        return f"{self.name}"


def publish_user_update(track: Track) -> None:
    publish('track_stored',
            {'id': track.user_id, 'tracks_qty': Track.objects.filter(user_id=track.user_id).count(),
             'tracks_length': Track.objects.filter(user_id=track.user_id).aggregate(ss=Sum('length')).get('ss', 0)})


@receiver(post_save, sender=Track)
def notify_about_new_user(instance: Track, created, *args, **kwargs) -> None:
    if created:
        publish_user_update(instance)
