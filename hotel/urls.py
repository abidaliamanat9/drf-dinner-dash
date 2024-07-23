from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, HotelViewSet


router = DefaultRouter()

router.register(r'category', viewset=CategoryViewSet)
router.register(r'hotel', viewset=HotelViewSet)
