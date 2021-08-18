from rest_framework import routers
from .views import (
    AuthorViewSet,
    BookViewSet,
    OrderViewSet
    )

app_name = 'API'

router = routers.DefaultRouter()
router.register('authors', AuthorViewSet, basename='authors')
router.register('books', BookViewSet, basename='books')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = router.urls
