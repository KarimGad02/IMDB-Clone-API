from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@example.com',
            'password1': 'testcasetestcase',
            'password2': 'testcasetestcase'
        }
        response = self.client.post(reverse('registration'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testcase', 
                                             password='testcasetestcase')

    def test_login(self):
        data = {
            'username': 'testcase',
            'password': 'testcasetestcase'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
