from django.urls import resolve, reverse
from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APITestCase

from ..views import HotelViewSet
from ..models import Hotel
from ..serializers import HotelSerializer


class HotelSerializerTestCase(APITestCase):
    def test_hotel_serialization(self):
        hotel = Hotel.objects.create(name="Test Hotel", phone="123-456-7890")
        serializer = HotelSerializer(hotel, context={'request': None})
        expected_data = {
            'url': f'/api/hotel/{hotel.id}/',
            'name': 'Test Hotel',
            'phone': '123-456-7890',
            'created_at': serializer.data['created_at'],
            'updated_at': serializer.data['updated_at'],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_hotel_deserialization(self):
        data = {'name': 'New Hotel', 'phone': '321-654-0987'}
        serializer = HotelSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        hotel = serializer.save()
        self.assertEqual(hotel.name, 'New Hotel')
        self.assertEqual(hotel.phone, '321-654-0987')


class HotelViewSetTestCase(APITestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name="Test Hotel", phone="123-456-7890")
        # Ensure this URL name matches your router
        self.list_url = reverse('hotel-list')
        self.detail_url = reverse('hotel-detail', kwargs={'pk': self.hotel.id})

    def test_list_hotels(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['results'][0]['name'], 'Test Hotel')

    def test_retrieve_hotel(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Hotel')

    def test_create_hotel(self):
        data = {'name': 'New Hotel', 'phone': '321-654-0987'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Hotel.objects.count(), 2)

    def test_update_hotel(self):
        data = {'name': 'Updated Hotel', 'phone': '555-555-5555'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hotel.refresh_from_db()
        self.assertEqual(self.hotel.name, 'Updated Hotel')
        self.assertEqual(self.hotel.phone, '555-555-5555')

    def test_delete_hotel(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hotel.objects.count(), 0)


class HotelURLSTestCase(SimpleTestCase):
    def test_hotel_url_resolves(self):
        view = resolve('/api/hotel/')
        self.assertEqual(view.func.cls, HotelViewSet)
