from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from user.models import UserProfile


class AccountViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.user_data = {
            'email': 'ravibhushan29@gmail.com',
            'first_name': 'Ravi',
            'last_name': 'Bhushan',
            'password': 'testpassword@123',
            'confirm_password': 'testpassword@123'
        }

    def test_create_account(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserProfile.objects.filter(email='ravibhushan29@gmail.com').exists())

    def test_password_mismatch(self):
        self.user_data['confirm_password'] = 'differentpassword@123'
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.user = UserProfile.objects.create_user(email='ravibhushan29@gmail.com',
                                                    password='testpassword@123')

    def test_login_successful(self):
        data = {
            'email': 'ravibhushan29@gmail.com',
            'password': 'testpassword@123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        data = {
            'email': 'ravibhushan29@gmail.com',
            'password': 'wrong@3435password'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
