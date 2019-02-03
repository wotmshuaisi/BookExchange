from rest_framework.routers import DefaultRouter
from api.viewsets.siteinfo import SiteinfoViewSet, BookCategoryViewSet
from api.viewsets.books import BooksInfoViewSet, MarkedBookViewSet, AddressViewSet, OrdersViewSet
from api.viewsets.users import UserViewset

from django.urls import path, include

router = DefaultRouter()

router.register(r'siteinfo', SiteinfoViewSet, basename='siteinfo')
router.register(r'category', BookCategoryViewSet, basename='category')
router.register(r'users', UserViewset, basename='users')
router.register(r'books', BooksInfoViewSet, basename='books')
router.register(r'marked', MarkedBookViewSet, basename='marked')
router.register(r'address', AddressViewSet, basename='address')
router.register(r'orders', OrdersViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]
