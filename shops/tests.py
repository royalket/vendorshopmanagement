from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import Vendor
from .models import Shop

class ShopAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create_user(
            email='test@example.com',
            name='Test Vendor',
            password='testpassword123'
        )
        self.shop_data = {
            'name': 'Test Shop',
            'owner': 'Test Owner',
            'business_type': 'Retail',
            'latitude': 28.7041,
            'longitude': 77.1025
        }
        self.client.force_authenticate(user=self.vendor)
    
    def test_create_shop(self):
        url = reverse('shop-list')
        response = self.client.post(url, self.shop_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shop.objects.count(), 1)
        self.assertEqual(Shop.objects.get().name, 'Test Shop')
        self.assertEqual(Shop.objects.get().vendor, self.vendor)
    
    def test_get_shop_list(self):
        # Create a shop
        Shop.objects.create(
            vendor=self.vendor,
            name='Test Shop',
            owner='Test Owner',
            business_type='Retail',
            latitude=28.7041,
            longitude=77.1025
        )
        
        url = reverse('shop-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Shop')
    
    def test_get_shop_detail(self):
        # Create a shop
        shop = Shop.objects.create(
            vendor=self.vendor,
            name='Test Shop',
            owner='Test Owner',
            business_type='Retail',
            latitude=28.7041,
            longitude=77.1025
        )
        
        url = reverse('shop-detail', kwargs={'pk': shop.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Shop')
    
    def test_update_shop(self):
        # Create a shop
        shop = Shop.objects.create(
            vendor=self.vendor,
            name='Test Shop',
            owner='Test Owner',
            business_type='Retail',
            latitude=28.7041,
            longitude=77.1025
        )
        
        updated_data = {
            'name': 'Updated Shop Name',
            'owner': 'Updated Owner',
            'business_type': 'Grocery',
            'latitude': 28.7042,
            'longitude': 77.1026
        }
        
        url = reverse('shop-detail', kwargs={'pk': shop.id})
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        shop.refresh_from_db()
        self.assertEqual(shop.name, 'Updated Shop Name')
        self.assertEqual(shop.business_type, 'Grocery')
    
    def test_delete_shop(self):
        # Create a shop
        shop = Shop.objects.create(
            vendor=self.vendor,
            name='Test Shop',
            owner='Test Owner',
            business_type='Retail',
            latitude=28.7041,
            longitude=77.1025
        )
        
        url = reverse('shop-detail', kwargs={'pk': shop.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Shop.objects.count(), 0)
    
    def test_unauthorized_access(self):
        # Create another vendor
        other_vendor = Vendor.objects.create_user(
            email='other@example.com',
            name='Other Vendor',
            password='otherpassword123'
        )
        
        # Create a shop for the other vendor
        shop = Shop.objects.create(
            vendor=other_vendor,
            name='Other Shop',
            owner='Other Owner',
            business_type='Retail',
            latitude=28.7041,
            longitude=77.1025
        )
        
        # Try to access the other vendor's shop
        url = reverse('shop-detail', kwargs={'pk': shop.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Try to update the other vendor's shop
        response = self.client.put(url, {'name': 'Hacked Shop'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Try to delete the other vendor's shop
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)