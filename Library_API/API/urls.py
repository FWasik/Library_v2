from rest_framework import routers
from .views import (AuthorViewSet, BookViewSet, OrderViewSet,
                    PublisherViewSet, GenreViewSet, DelivererViewSet,
                    AddressViewSet)

app_name = 'API'

router = routers.DefaultRouter()
router.register('authors', AuthorViewSet, basename='authors')
router.register('books', BookViewSet, basename='books')
router.register('orders', OrderViewSet, basename='orders')
router.register('publishers', PublisherViewSet, basename='publishers')
router.register('genres', GenreViewSet, basename='genres')
router.register('deliverers', DelivererViewSet, basename='deliverers')
router.register('addresses', AddressViewSet, basename='addresses')

urlpatterns = router.urls
