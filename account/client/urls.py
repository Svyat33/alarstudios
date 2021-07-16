from rest_framework import routers

from client.views import AccountView

router = routers.SimpleRouter()

router.register("users", AccountView, basename="account")

urlpatterns = router.urls