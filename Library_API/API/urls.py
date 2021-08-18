from rest_framework import routers
from .views import (
    AuthorViewSet,
    BookViewSet,
    OrderViewSet,
    UserViewSet
    )

app_name = 'API'

router = routers.DefaultRouter()
router.register('authors', AuthorViewSet, basename='authors')
router.register('books', BookViewSet, basename='books')
router.register('orders', OrderViewSet, basename='orders')
router.register('users', UserViewSet, basename='users')

urlpatterns = router.urls
