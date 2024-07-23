from rest_framework.routers import DefaultRouter

from hotel.urls import router as hotel_router

api_router = DefaultRouter()

api_router.registry.extend(*[
    hotel_router.registry
])
