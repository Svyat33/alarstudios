# Create your views here.
from decimal import Decimal

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from data.models import Dot, Track
from data.serializers import DotSerializer, TrackSerializerList, TrackDetailSerializer, TrackCreateSerializer
from dotstracks.settings import redis_instance


class DotsView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = DotSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Dot.objects.all()

    def get_queryset(self):
        if 'search_db' in self.request.query_params and 'radius' in self.request.query_params:
            lat, lon = self.request.query_params['search_db'].split(',')
            point = GEOSGeometry(f"POINT({Decimal(lat)} {Decimal(lon)})", srid=4326)
            from django.contrib.gis.db.models.functions import Distance
            return Dot.objects.all().annotate(distance=Distance("coord", point)).filter(
                coord__distance_lt=(point, D(km=self.request.query_params['radius']))) \
                .order_by("distance")
        if 'search' in self.request.query_params and 'radius' in self.request.query_params:
            lat, lon = self.request.query_params['search'].split(',')
            return Dot.objects.filter(pk__in=[int(id) for id in redis_instance.georadius("DOT", lon, lat,
                                                                                         self.request.query_params[
                                                                                             'radius'], unit='km')])
            point = GEOSGeometry(f"POINT({Decimal(lat)} {Decimal(lon)})", srid=4326)
            from django.contrib.gis.db.models.functions import Distance
            return Dot.objects.all().annotate(distance=Distance("coord", point)).filter(
                coord__distance_lt=(point, D(km=self.request.query_params['radius']))) \
                .order_by("distance")
        return Dot.objects.all()


class TrackView(mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                GenericViewSet):
    serializer_class = TrackSerializerList
    detail_serializer = TrackDetailSerializer
    create_serializer = TrackCreateSerializer
    queryset = Track.objects.all().select_related('user', )
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return self.create_serializer
        if self.request.method == "GET" and 'pk' in self.kwargs:
            return self.detail_serializer

        return self.serializer_class
