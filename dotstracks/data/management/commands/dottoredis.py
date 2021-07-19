import logging

from django.core.management.base import BaseCommand
from progress.bar import IncrementalBar

from data.models import Dot
from dotstracks.settings import redis_instance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Store all dots in Redis'

    def handle(self, *args, **options):

        logging.info("Store dot in Redis")
        bar = IncrementalBar("Store dots in Redis:", max=Dot.objects.all().count())
        redis_instance.delete("DOT")
        for d in Dot.objects.all():
            bar.next()
            redis_instance.geoadd("DOT", d.coord.y, d.coord.x, str(d.pk))
        print()

