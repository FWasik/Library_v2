from django.test import TestCase
from django.core.validators import ValidationError

from .models import (Author, Book, Publisher, Genre,
                    Deliverer, Address, Order)

from Authentication.models import CustomUser

from rest_framework import status
from Authentication.tests import APICustomUserTestCase
from django.urls import reverse


class ModelsTestCase(TestCase):
    def setUp(self):
        Author.objects.create(first_name='Andrzej', middle_name='', last_name='Sapkowski')

        Publisher.objects.create(name='Helion')

        Genre.objects.create(name='Fantasy')
        Genre.objects.create(name='Action')

        Deliverer.objects.create(name='DPD')

        address = Address.objects.create(street='Mickiewicza', number_of_building='23', number_of_apartment='',
                               city='Lublin', state='lubelskie', zip_code='23-100')
        try:
            address.full_clean()
        except ValidationError as exc:
            self.fail(exc)

    def models_tests(self):
        author = Author.objects.get(first_name='Andrzej', last_name='Sapkowski')

        publisher = Publisher.objects.get(name='Helion')

        genre_1 = Genre.objects.get(name='Fantasy')
        genre_2 = Genre.objects.get(name='Action')

        deliverer = Deliverer.objects.get(name='DPD')

        self.assertEqual(author.__str__(), 'Andrzej Sapkowski')
        self.assertEqual(publisher.__str__(), 'Helion')
        self.assertEqual(genre_1.__str__(), 'Fantasy')
        self.assertEqual(genre_2.__str__(), 'Action')
        self.assertEqual(deliverer.__str__(), 'DPD')

    def address_tests(self):
        address = Address.objects.get(street='Mickiewicza')

        self.assertEqual(address.street, 'Mickiewicza')
        self.assertEqual(address.number_of_building, '23')
        self.assertEqual(address.number_of_apartment, '')
        self.assertEqual(address.city, 'Lublin')
        self.assertEqual(address.state, 'lubelskie')
        self.assertEqual(address.zip_code, '23-100')

    def book_tests(self):
        author = Author.objects.get(first_name='Andrzej')
        publisher = Publisher.objects.get(name='Helion')
        #genre_1 = Genre.objects.get(name='Fantasy')
        #genre_2 = Genre.objects.get(name='Action')

        genres_book = Genre.objects.all()

        self.books = [Book.objects.create(title='Krew elfów', summary='', amount=20,
                            publisher=publisher, number_of_pages=300,
                            year_of_release=1994)]

        self.books[0].save()

        #self.book.author.set([Author.objects.get(first_name='Andrzej')])
        #self.book.genre.add(genre_1)
        #self.book.genre.add(genre_2)

        self.books[0].author.add(author)
        self.books[0].genre.add(*genres_book)

        genres_sample = ['Fantasy', 'Action']


        #print(self.book.author.all()[0])

        self.assertEqual(self.books[0].title, 'Krew elfów')
        self.assertEqual(self.books[0].summary, '')
        self.assertEqual(self.books[0].amount, 20)
        self.assertEqual(self.books[0].publisher.__str__(), 'Helion')
        self.assertEqual(self.books[0].number_of_pages, 300)
        self.assertEqual(self.books[0].year_of_release, 1994)
        self.assertEqual(self.books[0].author.get(first_name='Andrzej').__str__(), 'Andrzej Sapkowski')

        for (x, y) in zip(self.books[0].genre.all(), genres_sample):
            self.assertEqual(x.__str__(), y)


        #another book for order tests
        self.books.append(Book.objects.create(title='Ostatnie życzenie', summary='', amount=10,
                                         publisher=publisher, number_of_pages=200,
                                         year_of_release=1992))
        self.books[1].save()

    def order_tests(self):
        self.book_tests()

        user = CustomUser.objects.create_user(username='TestUser1', first_name='Test', middle_name='',
                                              last_name='User', email='TestUser1@email.com',
                                              PESEL='11111111111', phone_number='111111111')

        print(user)

        self.order = Order.objects.create(user=user, deliverer=Deliverer.objects.get(name='DPD'),
                                          address=Address.objects.get(street='Mickiewicza'))

        self.order.save()

        self.order.book.add(*self.books)

        print(self.order.date_order_create)

class APIAuthorTestCase(APICustomUserTestCase):
    url_detail = reverse('API:authors-detail', kwargs={'pk': 1})
    url_list = reverse('API:authors-list')

    def setUp(self) -> None:
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def create_author_test(self):
        self.assertEqual(self.url_list, '/api/authors/')

        data = {'first_name': 'Andrzej', 'middle_name': '', 'last_name': 'Sapkowski'}
        response = self.client.post(self.url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_authors_test(self):
        self.create_author_test()
        self.create_author_test()

        #retrieve
        self.assertEqual(self.url_detail, '/api/authors/1/')

        response = self.client.get(self.url_detail)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        self.assertEqual(self.url_list, '/api/authors/')

        response = self.client.get(self.url_list)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def partial_update_author_test(self):
        self.create_author_test()

        self.assertEqual(self.url_detail, '/api/authors/1/')

        data = {'first_name': 'Andrej'}
        response = self.client.patch(self.url_detail, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_author_test(self):
        self.create_author_test()

        self.assertEqual(self.url_detail, '/api/authors/1/')

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIPublisherTestCase(APICustomUserTestCase):
    url_detail = reverse('API:publishers-detail', kwargs={'pk': 1})
    url_list = reverse('API:publishers-list')

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def create_publisher_test(self):
        self.assertEqual(self.url_list, '/api/publishers/')

        data = {'name': 'Helion'}
        response = self.client.post(self.url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_publishers_test(self):
        self.create_publisher_test()
        self.create_publisher_test()

        #retrieve
        self.assertEqual(self.url_detail, '/api/publishers/1/')

        response = self.client.get(self.url_detail)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        self.assertEqual(self.url_list, '/api/publishers/')

        response = self.client.get(self.url_list)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def partial_update_publisher_test(self):
        self.create_publisher_test()

        self.assertEqual(self.url_detail, '/api/publishers/1/')

        data = {'name': 'Nova'}
        response = self.client.patch(self.url_detail, data, format='json')

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_publisher_test(self):
        self.create_publisher_test()

        self.assertEqual(self.url_detail, '/api/publishers/1/')

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIDelivererTestCase(APICustomUserTestCase):
    url_detail = reverse('API:deliverers-detail', kwargs={'pk': 1})
    url_list = reverse('API:deliverers-list')

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def create_deliverer_test(self):
        self.assertEqual(self.url_list, '/api/deliverers/')

        data = {'name': 'DPD'}
        response = self.client.post(self.url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_deliverers_test(self):
        self.create_deliverer_test()
        self.create_deliverer_test()

        #retrieve
        self.assertEqual(self.url_detail, '/api/deliverers/1/')

        response = self.client.get(self.url_detail)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        self.assertEqual(self.url_list, '/api/deliverers/')

        response = self.client.get(self.url_list)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def partial_update_deliverer_test(self):
        self.create_deliverer_test()

        self.assertEqual(self.url_detail, '/api/deliverers/1/')

        data = {'name': 'DHL'}
        response = self.client.patch(self.url_detail, data, format='json')

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_deliverer_test(self):
        self.create_deliverer_test()

        self.assertEqual(self.url_detail, '/api/deliverers/1/')

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIGenreTestCase(APICustomUserTestCase):
    url_detail = reverse('API:genres-detail', kwargs={'pk': 1})
    url_list = reverse('API:genres-list')

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def create_genre_test(self):
        self.assertEqual(self.url_list, '/api/genres/')

        data = {'name': 'Fantasy'}
        response = self.client.post(self.url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_genres_test(self):
        self.create_genre_test()
        self.create_genre_test()

        #retrieve
        self.assertEqual(self.url_detail, '/api/genres/1/')

        response = self.client.get(self.url_detail)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        self.assertEqual(self.url_list, '/api/genres/')

        response = self.client.get(self.url_list)

        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def partial_update_genre_test(self):
        self.create_genre_test()

        self.assertEqual(self.url_detail, '/api/genres/1/')

        data = {'name': 'Action'}
        response = self.client.patch(self.url_detail, data, format='json')

        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_genre_test(self):
        self.create_genre_test()

        self.assertEqual(self.url_detail, '/api/genres/1/')

        response = self.client.delete(self.url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

