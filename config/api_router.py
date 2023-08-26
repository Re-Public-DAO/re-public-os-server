from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from republic_os.users.api.views import UserViewSet
from republic_os.apps.api.views import AppInstallViewSet
from republic_os.devices.api.views import DeviceViewSet
from republic_os.connectors.api.views import OAuthStateViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("apps", AppInstallViewSet)
router.register("devices", DeviceViewSet)
router.register("oauth", OAuthStateViewSet)


app_name = "api"
urlpatterns = router.urls
