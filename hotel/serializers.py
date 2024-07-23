from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Hotel


class CategroySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            if 'unique_category_name_ci' in str(e):
                raise ValidationError(
                    {"name": ["This category name already exists."]}
                )
            else:
                raise e


class HotelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"
