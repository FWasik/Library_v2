from .views import UserViewSet
from rest_framework import routers

app_name = 'Authentication'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls
