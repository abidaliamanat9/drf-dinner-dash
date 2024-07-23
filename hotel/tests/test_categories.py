from django.test import TestCase
from django.urls import reverse, resolve
from django.test import SimpleTestCase

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.routers import DefaultRouter


from ..models import Category
from ..serializers import CategroySerializer
from ..views import CategoryViewSet


class CategorySerializerTestCase(APITestCase):
    def test_category_serialization(self):
        category = Category.objects.create(name="Test Category")
        serializer = CategroySerializer(category, context={'request': None})
        expected_data = {
            'url': f'/api/category/{category.id}/',
            'name': 'Test Category',
            'created_at': serializer.data['created_at'],
            'updated_at': serializer.data['updated_at'],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_category_deserialization(self):
        data = {'name': 'New Category'}
        serializer = CategroySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        category = serializer.save()
        self.assertEqual(category.name, 'New Category')


class CategoryViewSetTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.list_url = reverse('category-list')
        self.detail_url = reverse(
            'category-detail', kwargs={'pk': self.category.id})

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['results'][0]['name'], 'Test Category')

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_create_category(self):
        data = {'name': 'New Category'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_update_category(self):
        data = {'name': 'Updated Category'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category')

    def test_delete_category(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)


class CategoryModelTestCase(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Unique Name")
        self.assertEqual(str(category), "Unique Name")

    def test_category_unique_constraint(self):
        Category.objects.create(name="CaseInsensitive")
        with self.assertRaises(Exception):
            Category.objects.create(name="caseinsensitive")


class CategoryURLSTestCase(SimpleTestCase):
    def test_category_url_resolves(self):
        router = DefaultRouter()
        router.register(r'category', viewset=CategoryViewSet)
        resolver = router.urls[0]
        view = resolve('/api/category/')
        self.assertEqual(view.func.cls, CategoryViewSet)
