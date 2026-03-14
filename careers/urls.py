from rest_framework.routers import DefaultRouter

from .views import PostViewSet

router = DefaultRouter()
router.register(r"careers", PostViewSet, basename="careers")

urlpatterns = router.urls
