
from Authentication.models import CustomUser

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY

class APICustomUserTestCase(APITestCase):
    url_detail = reverse('Authentication:users-detail', kwargs={'username': 'TestUser1'})
    url_list = reverse('Authentication:users-list')

    def create_user_test(self):
        self.assertEqual(self.url_list, '/api/auth/users/')

        data = {'username': 'TestUser1', 'first_name': 'Test', 'middle_name': '',
                'last_name': 'User', 'is_staff': True, 'email': 'TestUser1@email.com',
                'PESEL': '11111111111', 'phone_number': '111111111',
                'password': 'TestUser1!', 'password1': 'TestUser1!'}

        '''
        response = self.client.post(url, data=encode_multipart(data=data, boundary=BOUNDARY),
                                    content_type=MULTIPART_CONTENT)
        '''

        response = self.client.post(self.url_list, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def auth_user_test(self):
        self.create_user_test()

        url = reverse('token_obtain_pair')
        data = {'username': 'TestUser1', 'password': 'TestUser1!'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return response.json()['access']

    def get_users_test(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

        #retrieve
        self.assertEqual(self.url_detail, '/api/auth/users/TestUser1/')

        response = self.client.get(self.url_detail)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        data = {'username': 'TestUser2', 'first_name': 'Test', 'middle_name': '',
                'last_name': 'User', 'is_staff': True, 'email': 'TestUser2@email.com',
                'PESEL': '22222222222', 'phone_number': '222222222',
                'password': 'TestUser2!', 'password1': 'TestUser2!'}

        self.client.post(self.url_list, data, format='multipart')

        response = self.client.get(self.url_list)

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def partial_update_user_test(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertEqual(self.url_detail, '/api/auth/users/TestUser1/')

        response = self.client.patch(self.url_detail, {'middle_name': '1'}, format='multipart')

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_user_test(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertEqual(self.url_detail, '/api/auth/users/TestUser1/')

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
