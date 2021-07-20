import logging

from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from data.notifier import publish

logger = logging.getLogger(__name__)


class Dot(models.Model):
    coord = models.PointField()
    name = models.CharField(max_length=200)

    def __repr__(self):
        return f"{self.name} {self.coord.x},{self.coord.y}"


class Track(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dots = models.ManyToManyField(Dot)
    length = models.IntegerField(default=0)

    @property
    def begin(self):
        return self.dots.through.objects.filter(track_id=self.pk).order_by('id')[0].dot

    @property
    def end(self):
        return self.dots.through.objects.filter(track_id=self.pk).order_by('-id')[0].dot

    @property
    def track(self):
        return [tdconn.dot for tdconn in
                self.dots.through.objects.filter(track_id=self.pk).select_related('dot').order_by('id')]

    def __repr__(self):
        return f"{self.name}"


def publish_track_created(track: Track) -> None:
    publish('track_stored',
            {'id': track.user_id, 'tracks_qty': Track.objects.filter(user_id=track.user_id).count(),
             'tracks_length': Track.objects.filter(user_id=track.user_id).aggregate(ss=Sum('length')).get('ss', 0)})


@receiver(post_save, sender=Track)
def notify_about_new_track(instance: Track, created, *args, **kwargs) -> None:
    if created:
        publish_track_created(instance)
