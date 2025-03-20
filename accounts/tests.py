from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Vendor

class VendorRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')
        self.vendor_data = {
            'email': 'test@example.com',
            'name': 'Test Vendor',
            'password': 'testpassword123'
        }

    def test_register_vendor(self):
        response = self.client.post(self.register_url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('user' in response.data)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().email, 'test@example.com')

    def test_login_vendor(self):
        # Create a vendor first
        Vendor.objects.create_user(
            email='test@example.com',
            name='Test Vendor',
            password='testpassword123'
        )
        
        # Login with the credentials
        login_data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

class VendorProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create_user(
            email='test@example.com',
            name='Test Vendor',
            password='testpassword123'
        )
        self.profile_url = reverse('vendor_profile')

    def test_get_vendor_profile(self):
        self.client.force_authenticate(user=self.vendor)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['name'], 'Test Vendor')

    def test_update_vendor_profile(self):
        self.client.force_authenticate(user=self.vendor)
        updated_data = {
            'name': 'Updated Vendor Name'
        }
        response = self.client.put(self.profile_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Vendor Name')
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, 'Updated Vendor Name')