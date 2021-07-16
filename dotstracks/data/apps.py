import logging

import redis as redis
from django.apps import AppConfig
from progress.bar import IncrementalBar
from dotstracks import settings

logger = logging.getLogger(__name__)


class DataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data'

    # def ready(self):
    #     redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    #     logging.info("Store dot in Redis")
    #     from data.models import Dot
    #     bar = IncrementalBar("Store dots in Redis:", max=Dot.objects.all())
    #     for d in Dot.objects.all():
    #          redis_instance.geoadd("DOT", d.coord.y, d.coord.x, str(d.pk))
    #          bar.next(1)
