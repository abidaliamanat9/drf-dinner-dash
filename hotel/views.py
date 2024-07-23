from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Category, Hotel
from .serializers import CategroySerializer, HotelSerializer

from .pagination import CustomCursorPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategroySerializer
    pagination_class = CustomCursorPagination


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    pagination_class = CustomCursorPagination