
import logging
import random

import faker
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from data.models import Dot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Generate random dots'

    def handle(self, *args, **options):
        fake = faker.Faker(locale='en')
        Dot.objects.bulk_create(
            (Dot(coord=Point(random.randint(-8500000, 8500000)/100000, random.randint(-18000000, 18000000)/100000),
            name=fake.address()) for _ in range(500_000)),
            batch_size=200
        )

