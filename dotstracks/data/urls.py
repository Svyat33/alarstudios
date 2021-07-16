from rest_framework import routers

from .views import DotsView, TrackView

router = routers.SimpleRouter()

router.register("dot", DotsView, basename="dots")
router.register("track", TrackView, basename="track")
urlpatterns = router.urls