from django.test import TestCase
from django.core.validators import ValidationError

from .models import (Author, Book, Publisher, Genre,
                    Deliverer, Address, Order)

from Authentication.models import CustomUser

from rest_framework import status
from Authentication.tests import APICustomUserTestCase
from django.urls import reverse

from .serializers import (AuthorSerializer,
                          PublisherSerializer,
                          DelivererSerializer,
                          GenreSerializer,
                          AddressSerializer,
                          BookSerializer,
                          OrderSerializer)


class ModelsTestCase(TestCase):
    def setUp(self):
        Author.objects.create(first_name='Andrzej', middle_name='', last_name='Sapkowski')

        Publisher.objects.create(name='Helion')

        Genre.objects.create(name='Fantasy')
        Genre.objects.create(name='Action')

        Deliverer.objects.create(name='DPD')

        address = Address.objects.create(street='Mickiewicza',
                                         number_of_building='23',
                                         number_of_apartment='',
                                         city='Lublin',
                                         state='lubelskie',
                                         zip_code='23-100')
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

        self.books = [Book.objects.create(title='Krew elfów',
                                          summary='',
                                          amount=20,
                                          publisher=publisher,
                                          number_of_pages=300,
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
        self.books.append(Book.objects.create(title='Ostatnie życzenie',
                                              summary='',
                                              amount=10,
                                              publisher=publisher,
                                              number_of_pages=200,
                                              year_of_release=1992))
        self.books[1].save()

    def order_tests(self):
        self.book_tests()

        user = CustomUser.objects.create_user(username='TestUser1',
                                              first_name='Test',
                                              middle_name='',
                                              last_name='User',
                                              email='TestUser1@email.com',
                                              PESEL='11111111111',
                                              phone_number='111111111')

        print(user)

        self.order = Order.objects.create(user=user,
                                          deliverer=Deliverer.objects.get(name='DPD'),
                                          address=Address.objects.get(street='Mickiewicza'))

        self.order.save()

        self.order.book.add(*self.books)

        print(self.order.date_order_create)


author_url_list = reverse('API:authors-list')

publisher_url_list = reverse('API:publishers-list')

deliverer_url_list = reverse('API:deliverers-list')

genre_url_list = reverse('API:genres-list')

address_url_list = reverse('API:addresses-list')

book_url_list = reverse('API:books-list')

order_url_list = reverse('API:orders-list')


class APIBaseTestCase(APICustomUserTestCase):
    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')


class APIBasicAuthorTestCase(APIBaseTestCase):
    def setUp(self):
        super().setUp()

        self.author = Author.objects.create(first_name='Andrzej',
                                            middle_name='',
                                            last_name='Sapkowski')

        Author.objects.create(first_name='George',
                              middle_name='R.R.',
                              last_name='Martin')

        self.valid_payload_create = {
            'first_name': 'Carl',
            'middle_name': '',
            'last_name': 'Sagan'
        }

        self.valid_payload_update = {
            'first_name': 'Jarosław',
            'middle_name': '',
            'last_name': 'Grzędowicz'
        }

        self.invalid_payload = {
            'first_name': '',
            'middle_name': '',
            'last_name': ''
        }

        self.author_url_detail = reverse('API:authors-detail', kwargs={'pk': self.author.pk})


class APIPOSTAuthorTestCase(APIBasicAuthorTestCase):
    def test_create_valid_author(self):
        response = self.client.post(author_url_list, self.valid_payload_create, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_author(self):
        response = self.client.post(author_url_list, self.invalid_payload, format='json')

        # print(response)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIGETAuthorTestCase(APIBasicAuthorTestCase):
    def test_get_all_authors(self):
        response = self.client.get(author_url_list)
        serializer = AuthorSerializer(Author.objects.all(), many=True)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_author(self):
        response = self.client.get(self.author_url_detail)
        serializer = AuthorSerializer(self.author)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_author(self):
        response = self.client.get(reverse('API:authors-detail', kwargs={'pk': 20}))

        # print(response)
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class APIPATCHAuthorTestCase(APIBasicAuthorTestCase):
    def test_patch_valid_author(self):
        response = self.client.patch(self.author_url_detail, self.valid_payload_update, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_author(self):
        response = self.client.patch(self.author_url_detail, self.invalid_payload, format='json')

        # print(response.json())
        # print(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIDELETEAuthorTestCase(APIBasicAuthorTestCase):
    def test_delete_valid_author(self):
        response = self.client.delete(self.author_url_detail)

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_author(self):
        response = self.client.patch(reverse('API:authors-detail', kwargs={'pk': 25}))

        # print(response.json())
        # print(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


########################################################################################################


class APIBasicPublisherTestCase(APIBaseTestCase):
    def setUp(self):
        super().setUp()

        self.publisher = Publisher.objects.create(name='Helion')
        Publisher.objects.create(name='Nova')

        self.valid_payload_create = {
            'name': 'Jedność'
        }

        self.valid_payload_update = {
            'name': 'Amazon'
        }

        self.invalid_payload = {
            'name': ''
        }

        self.publisher_url_detail = reverse('API:publishers-detail', kwargs={'pk': self.publisher.pk})


class APIPOSTPublisherTestCase(APIBasicPublisherTestCase):
    def test_create_valid_publisher(self):
        response = self.client.post(publisher_url_list, self.valid_payload_create, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_publisher(self):
        response = self.client.post(publisher_url_list, self.invalid_payload, format='json')

        # print(response)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIGETPublisherTestCase(APIBasicPublisherTestCase):
    def test_get_all_publishers(self):
        response = self.client.get(publisher_url_list)
        serializer = PublisherSerializer(Publisher.objects.all(), many=True)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_publisher(self):
        response = self.client.get(self.publisher_url_detail)
        serializer = PublisherSerializer(self.publisher)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_publisher(self):
        response = self.client.get(reverse('API:publishers-detail', kwargs={'pk': 20}))

        # print(response)
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class APIPATCHPublisherTestCase(APIBasicPublisherTestCase):
    def test_patch_valid_publisher(self):
        response = self.client.patch(self.publisher_url_detail, self.valid_payload_update, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_publisher(self):
        response = self.client.patch(self.publisher_url_detail, self.invalid_payload, format='json')

        # print(response.json())
        # print(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIDELETEPublisherTestCase(APIBasicPublisherTestCase):
    def test_delete_valid_publisher(self):
        response = self.client.delete(self.publisher_url_detail)

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_publisher(self):
        response = self.client.patch(reverse('API:publishers-detail', kwargs={'pk': 25}))

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


########################################################################################################


class APIBasicDelivererTestCase(APIBaseTestCase):
    def setUp(self):
        super().setUp()

        self.deliverer = Deliverer.objects.create(name='DPD')
        Deliverer.objects.create(name='DHL')

        self.valid_payload_create = {
            'name': 'Poczta Polska'
        }

        self.valid_payload_update = {
            'name': 'UPC'
        }

        self.invalid_payload = {
            'name': ''
        }

        self.deliverer_url_detail = reverse('API:deliverers-detail', kwargs={'pk': self.deliverer.pk})


class APIPOSTDelivererTestCase(APIBasicDelivererTestCase):
    def test_create_valid_deliverer(self):
        response = self.client.post(deliverer_url_list, self.valid_payload_create, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_deliverer(self):
        response = self.client.post(deliverer_url_list, self.invalid_payload, format='json')

        # print(response)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIGETDelivererTestCase(APIBasicDelivererTestCase):
    def test_get_all_deliverers(self):
        response = self.client.get(deliverer_url_list)
        serializer = DelivererSerializer(Deliverer.objects.all(), many=True)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_deliverer(self):
        response = self.client.get(self.deliverer_url_detail)
        serializer = DelivererSerializer(self.deliverer)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIPATCHDelivererTestCase(APIBasicDelivererTestCase):
    def test_patch_valid_deliverer(self):
        response = self.client.patch(self.deliverer_url_detail, self.valid_payload_update, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_deliverer(self):
        response = self.client.patch(self.deliverer_url_detail, self.invalid_payload, format='json')

        # print(response.json())
        # print(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIDELETEDelivererTestCase(APIBasicDelivererTestCase):
    def test_delete_valid_deliverer(self):
        response = self.client.delete(self.deliverer_url_detail)

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_deliverer(self):
        response = self.client.delete('API:deliverers-detail', kwargs={'pk': 40})

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


########################################################################################################


class APIBasicGenreTestCase(APIBaseTestCase):
    def setUp(self):
        super().setUp()

        self.genre = Genre.objects.create(name='Fantasy')
        Genre.objects.create(name='Action')

        self.valid_payload_create = {
            'name': 'Thriller'
        }

        self.valid_payload_update = {
            'name': 'Romance'
        }

        self.invalid_payload = {
            'name': ''
        }

        self.genre_url_detail = reverse('API:genres-detail', kwargs={'pk': self.genre.pk})


class APIPOSTGenreTestCase(APIBasicGenreTestCase):
    def test_create_valid_genre(self):
        response = self.client.post(genre_url_list, self.valid_payload_create, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_genre(self):
        response = self.client.post(genre_url_list, self.invalid_payload, format='json')

        # print(response)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIGETGenreTestCase(APIBasicGenreTestCase):
    def test_get_all_genres(self):
        response = self.client.get(genre_url_list)
        serializer = GenreSerializer(Genre.objects.all(), many=True)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_genre(self):
        response = self.client.get(self.genre_url_detail)
        serializer = GenreSerializer(self.genre)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIPATCHGenreTestCase(APIBasicGenreTestCase):
    def test_patch_valid_genre(self):
        response = self.client.patch(self.genre_url_detail, self.valid_payload_update, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_genre(self):
        response = self.client.patch(self.genre_url_detail, self.invalid_payload, format='json')

        # print(response.json())
        # print(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIDELETEGenreTestCase(APIBasicGenreTestCase):
    def test_delete_valid_genre(self):
        response = self.client.delete(self.genre_url_detail)

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_genre(self):
        response = self.client.delete('API:genres-detail', kwargs={'pk': 20})

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


########################################################################################################

class APIBasicAddressTestCase(APIBaseTestCase):
    def setUp(self):
        super().setUp()

        self.address = Address.objects.create(street='Mickiewicza',
                                         number_of_building='23',
                                         number_of_apartment='',
                                         city='Lublin',
                                         state='lubelskie',
                                         zip_code='23-100')

        Address.objects.create(street='Sienkiewicza',
                               number_of_building='2',
                               number_of_apartment='30',
                               city='Warszawa',
                               state='mazowieckie',
                               zip_code='40-204')

        self.valid_payload_create = {
            'street': 'Piłsudskiego',
            'number_of_building': '21',
            'number_of_apartment': '100',
            'city': 'Gdańsk',
            'state': 'pomorskie',
            'zip_code': '24-542'
        }

        self.valid_payload_update = {
            'street': 'Aleje Racławickie',
            'number_of_building': '15',
            'number_of_apartment': '142',
            'city': 'Lublin',
            'state': 'lubelskie',
            'zip_code': '45-241'
        }

        self.invalid_payload = {
            'street': 'Jana Pawła II',
            'number_of_building': '21fdf',
            'number_of_apartment': '1ggfg',
            'city': 'Gdańsk',
            'state': 'pomorskie',
            'zip_code': '24-542fgv3'
        }

        self.address_url_detail = reverse('API:addresses-detail', kwargs={'pk': self.address.pk})


class APIPOSTAddressTestCase(APIBasicAddressTestCase):
    def test_create_valid_address(self):
        response = self.client.post(address_url_list, self.valid_payload_create, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_address(self):
        response = self.client.post(address_url_list, self.invalid_payload, format='json')

        # print(response)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIGETAddressTestCase(APIBasicAddressTestCase):
    def test_get_all_address(self):
        response = self.client.get(address_url_list)
        serializer = AddressSerializer(Address.objects.all(), many=True)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_address(self):
        response = self.client.get(self.address_url_detail)
        serializer = AddressSerializer(self.address)

        # print(serializer.data)
        # print(response.data)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIPATCHAddressTestCase(APIBasicAddressTestCase):
    def test_patch_valid_address(self):
        response = self.client.patch(self.address_url_detail, self.valid_payload_update, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_address(self):
        response = self.client.patch(self.address_url_detail, self.invalid_payload, format='json')

        # print(response.json())
        # print(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIDELETEAddressTestCase(APIBasicAddressTestCase):
    def test_delete_valid_address(self):
        response = self.client.delete(self.address_url_detail)

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_address(self):
        response = self.client.delete('API:addresses-detail', kwargs={'pk': 18})

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


########################################################################################################


class APIBasicBookTestCase(APIBaseTestCase):
    def setUp(self):
        super().setUp()

        self.author_1 = Author.objects.create(first_name='Andrzej',
                                            middle_name='',
                                            last_name='Sapkowski')

        self.author_2 = Author.objects.create(first_name='George',
                                            middle_name='R.R.',
                                            last_name='Martin')

        self.publisher_1 = Publisher.objects.create(name='Helion')
        self.publisher_2 = Publisher.objects.create(name='Nova')

        self.genre_1 = Genre.objects.create(name='Fantasy')
        self.genre_2 = Genre.objects.create(name='Action')


        self.book_1 = Book.objects.create(title='Krew elfów',
                                          summary='',
                                          amount=20,
                                          publisher=self.publisher_1,
                                          number_of_pages=300,
                                          year_of_release=1994)

        self.book_1.author.add(self.author_1)
        self.book_1.genre.add(self.genre_1)
        self.book_1.genre.add(self.genre_2)

        self.book_2 = Book.objects.create(title='Gra o tron',
                                          summary='',
                                          amount=30,
                                          publisher=self.publisher_2,
                                          number_of_pages=350,
                                          year_of_release=1996)

        self.book_2.author.add(self.author_2)
        self.book_2.genre.add(self.genre_1)
        self.book_2.genre.add(self.genre_2)


        self.valid_payload_create = {
            'title': 'Ostatnie życzenie',
            'summary': '',
            'author': [self.author_1.pk],
            'publisher': self.publisher_1.pk,
            'amount': 40,
            'genre': [self.genre_1.pk, self.genre_2.pk],
            'number_of_pages': 250,
            'year_of_release': 1995
        }

        self.valid_payload_update = {
            'number_of_pages': 500,
            'amount': 100
        }

        self.invalid_payload = {
            'title': 'Starcie królów',
            'summary': '',
            'author': [self.author_1.pk],
            'publisher': self.publisher_1.pk,
            'amount': 'gfgfgf',
            'genre': [self.genre_1.pk, self.genre_2.pk],
            'number_of_pages': 'ythyj',
            'year_of_release': '2r423'
        }

        self.book_url_detail = reverse('API:books-detail', kwargs={'pk': self.book_1.pk})


class APIPOSTBookTestCase(APIBasicBookTestCase):
    def test_create_valid_book(self):
        response = self.client.post(book_url_list, self.valid_payload_create, format='json')

        # print(response)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_book(self):
        response = self.client.post(book_url_list, self.invalid_payload, format='json')

        # print(response)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIGETBookTestCase(APIBasicBookTestCase):
    def test_get_all_books(self):
        response = self.client.get(book_url_list)
        serializer = BookSerializer(Book.objects.all(), many=True)

        # print(serializer.data)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_book(self):
        response = self.client.get(self.book_url_detail)
        serializer = BookSerializer(self.book_1)

        # print(serializer.data)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIPATCHBookTestCase(APIBasicBookTestCase):
    def test_patch_valid_book(self):
        response = self.client.patch(self.book_url_detail, self.valid_payload_update, format='json')

        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_invalid_book(self):
        response = self.client.patch(self.book_url_detail, self.invalid_payload, format='json')

        # print(response.json())
        # print(response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIDELETEBookTestCase(APIBasicBookTestCase):
    def test_delete_valid_book(self):
        response = self.client.delete(self.book_url_detail)

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_book(self):
        response = self.client.delete('API:books-detail', kwargs={'pk': 40})

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


########################################################################################################


class APIBasicOrderTestCase(APIBasicBookTestCase):
    def setUp(self):
        super().setUp()

        self.deliverer_1 = Deliverer.objects.create(name='DPD')
        self.deliverer_2 = Deliverer.objects.create(name='DHL')

        self.address_1 = Address.objects.create(street='Mickiewicza',
                                                  number_of_building='23',
                                                  number_of_apartment='',
                                                  city='Lublin',
                                                  state='lubelskie',
                                                  zip_code='23-100')

        self.address_2 = Address.objects.create(street='Sienkiewicza',
                                                   number_of_building='2',
                                                   number_of_apartment='30',
                                                   city='Warszawa',
                                                   state='mazowieckie',
                                                   zip_code='40-204')

        self.user = CustomUser.objects.get(username='TestUser1')

        self.order_1 = Order.objects.create(user=self.user,
                                            deliverer=self.deliverer_1,
                                            address=self.address_1)

        self.order_1.book.add(self.book_1)

        self.order_2 = Order.objects.create(user=self.user,
                                            deliverer=self.deliverer_2,
                                            address=self.address_1)

        self.order_2.book.add(self.book_1)
        self.order_2.book.add(self.book_2)


        self.order_3 = Order.objects.create(user=self.user,
                                            deliverer=self.deliverer_2,
                                            address=self.address_2)

        self.order_3.book.add(self.book_1)


        self.valid_payload_create = {
            'deliverer': self.deliverer_1.pk,
            'book': [self.book_1.pk, self.book_2.pk],
            'address': {
                'street': 'Aleje Racławickie',
                'number_of_building': '15',
                'number_of_apartment': '142',
                'city': 'Lublin',
                'state': 'lubelskie',
                'zip_code': '45-241'
            }
        }

        self.invalid_payload = {
            'deliverer': self.deliverer_2.pk,
            'book': [self.book_2.pk],
            'address': {
                'street': 'Aleje Racławickie',
                'number_of_building': '15',
                'number_of_apartment': '142gfgf',
                'city': 'Lublin',
                'state': 'lubelskie',
                'zip_code': '45-241gfgd'
            }
        }

        self.order_url_detail = reverse('API:orders-detail', kwargs={'pk': self.order_1.pk})


class APIPOSTOrderTestCase(APIBasicOrderTestCase):
    def test_create_valid_order(self):
        response = self.client.post(order_url_list, self.valid_payload_create, format='json')

        # print(response)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_order(self):
        response = self.client.post(order_url_list, self.invalid_payload, format='json')

        # print(response)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class APIGETOrderTestCase(APIBasicOrderTestCase):
    def test_get_all_orders(self):
        response = self.client.get(order_url_list)
        serializer = OrderSerializer(Order.objects.all(), many=True)

        # print(serializer.data)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_order(self):
        response = self.client.get(self.order_url_detail)
        serializer = OrderSerializer(self.order_1)

        # print(serializer.data)
        # print(response.data)
        # print(response.json())

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIDELETEOrderTestCase(APIBasicOrderTestCase):
    def test_delete_valid_order_without_address(self):
        response = self.client.delete(self.order_url_detail)

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse('API:addresses-detail', kwargs={'pk': self.address_1.pk}))

        # print(response)
        # print(response.json())

        #that address is assigned to more than just one order so it is no deleted
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_valid_order_with_address(self):
        response = self.client.delete(reverse('API:orders-detail', kwargs={'pk': self.order_3.pk}))

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse('API:addresses-detail', kwargs={'pk': self.address_2.pk}))

        # print(response)
        # print(response.json())

        #that address was assigned to only one, just deleted, order so it was deleted too
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invalid_order(self):
        response = self.client.delete('API:orders-detail', kwargs={'pk': 50})

        # print(response)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



'''
class APIAuthorTestCase(APICustomUserTestCase):
    author_pk = None

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_create_author(self):
        self.assertEqual(author_url_list, '/api/authors/')

        data = {'first_name': 'Andrzej', 'middle_name': '', 'last_name': 'Sapkowski'}
        response = self.client.post(author_url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #print(response.json())

        self.author_pk = response.json()['id']

    def test_get_authors(self):
        self.test_create_author()
        self.test_create_author()

        author_url_detail = reverse('API:authors-detail', kwargs={'pk': self.author_pk})

        #retrieve
        self.assertEqual(author_url_detail, f'/api/authors/{self.author_pk}/')

        response = self.client.get(author_url_detail)
        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        response = self.client.get(author_url_list)
        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_author(self):
        self.test_create_author()

        author_url_detail = reverse('API:authors-detail', kwargs={'pk': self.author_pk})

        self.assertEqual(author_url_detail, f'/api/authors/{self.author_pk}/')

        data = {'first_name': 'Andrej'}
        response = self.client.patch(author_url_detail, data, format='json')
        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_author(self):
        self.test_create_author()

        author_url_detail = reverse('API:authors-detail', kwargs={'pk': self.author_pk})

        self.assertEqual(author_url_detail, f'/api/authors/{self.author_pk}/')

        response = self.client.delete(author_url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIPublisherTestCase(APICustomUserTestCase):
    publisher_pk = None

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_create_publisher(self):
        self.assertEqual(publisher_url_list, '/api/publishers/')

        data = {'name': 'Helion'}
        response = self.client.post(publisher_url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #print(response.json())

        self.publisher_pk = response.json()['id']

    def test_get_publishers(self):
        self.test_create_publisher()
        self.test_create_publisher()

        publisher_url_detail = reverse('API:publishers-detail', kwargs={'pk': self.publisher_pk})

        #retrieve
        self.assertEqual(publisher_url_detail, f'/api/publishers/{self.publisher_pk}/')

        response = self.client.get(publisher_url_detail)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        response = self.client.get(publisher_url_list)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_publisher(self):
        self.test_create_publisher()

        publisher_url_detail = reverse('API:publishers-detail', kwargs={'pk': self.publisher_pk})

        self.assertEqual(publisher_url_detail, f'/api/publishers/{self.publisher_pk}/')

        data = {'name': 'Nova'}
        response = self.client.patch(publisher_url_detail, data, format='json')

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_publisher(self):
        self.test_create_publisher()

        publisher_url_detail = reverse('API:publishers-detail', kwargs={'pk': self.publisher_pk})

        self.assertEqual(publisher_url_detail, f'/api/publishers/{self.publisher_pk}/')

        response = self.client.delete(publisher_url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIDelivererTestCase(APICustomUserTestCase):
    deliverer_pk = None

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_create_deliverer(self):
        self.assertEqual(deliverer_url_list, '/api/deliverers/')

        data = {'name': 'DPD'}
        response = self.client.post(deliverer_url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #print(response.json())

        self.deliverer_pk = response.json()['id']

    def test_get_deliverers(self):
        self.test_create_deliverer()
        self.test_create_deliverer()

        deliverer_url_detail = reverse('API:deliverers-detail', kwargs={'pk': self.deliverer_pk})

        #retrieve
        self.assertEqual(deliverer_url_detail, f'/api/deliverers/{self.deliverer_pk}/')

        response = self.client.get(deliverer_url_detail)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        response = self.client.get(deliverer_url_list)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_deliverer(self):
        self.test_create_deliverer()

        deliverer_url_detail = reverse('API:deliverers-detail', kwargs={'pk': self.deliverer_pk})

        self.assertEqual(deliverer_url_detail, f'/api/deliverers/{self.deliverer_pk}/')

        data = {'name': 'DHL'}
        response = self.client.patch(deliverer_url_detail, data, format='json')

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_deliverer(self):
        self.test_create_deliverer()

        deliverer_url_detail = reverse('API:deliverers-detail', kwargs={'pk': self.deliverer_pk})

        self.assertEqual(deliverer_url_detail, f'/api/deliverers/{self.deliverer_pk}/')

        response = self.client.delete(deliverer_url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIGenreTestCase(APICustomUserTestCase):

    genre_pk = None

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_create_genre(self):
        self.assertEqual(genre_url_list, '/api/genres/')

        data = {'name': 'Fantasy'}
        response = self.client.post(genre_url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #print(response.json())

        self.genre_pk = response.json()['id']

    def test_get_genres(self):
        self.test_create_genre()
        self.test_create_genre()

        genre_url_detail = reverse('API:genres-detail', kwargs={'pk': self.genre_pk})

        #retrieve
        self.assertEqual(genre_url_detail, f'/api/genres/{self.genre_pk}/')

        response = self.client.get(genre_url_detail)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #list
        response = self.client.get(genre_url_list)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_genre(self):
        self.test_create_genre()

        genre_url_detail = reverse('API:genres-detail', kwargs={'pk': self.genre_pk})

        self.assertEqual(genre_url_detail, f'/api/genres/{self.genre_pk}/')

        data = {'name': 'Action'}
        response = self.client.patch(genre_url_detail, data, format='json')

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_genre(self):
        self.test_create_genre()

        genre_url_detail = reverse('API:genres-detail', kwargs={'pk': self.genre_pk})

        self.assertEqual(genre_url_detail, f'/api/genres/{self.genre_pk}/')

        response = self.client.delete(genre_url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIAddressTestCase(APICustomUserTestCase):
    address_pk = None

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_create_address(self):
        self.assertEqual(address_url_list, '/api/addresses/')

        data = {'street': 'Mickiewicza',
                'number_of_building': '23',
                'number_of_apartment': '',
                'city': 'Lublin',
                'state': 'lubelskie',
                'zip_code': '23-100'}

        self.assertRegex(data['street'], '^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó -]{1,100}$')
        self.assertRegex(data['number_of_building'], '^[0-9]{1,5}$')
        self.assertRegex(data['city'], '^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó -]{1,100}$')
        self.assertRegex(data['state'], '^[a-zA-ZŻŹĆĄŚĘŃŁÓżźćąśęńłó -]{1,100}$')
        self.assertRegex(data['zip_code'], '^\d{2}-\d{3}$')

        if not data['number_of_apartment'] == '':
            self.assertRegex(data['number_of_apartment'], '^[0-9]{1,5}$')

        response = self.client.post(address_url_list, data, format='json')

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.address_pk = response.json()['id']

    def test_get_addresses(self):
        #creating identical addresses from the level of address view/class is allowed
        self.test_create_address()

        address_url_detail = reverse('API:addresses-detail', kwargs={'pk': self.address_pk})

        # retrieve
        self.assertEqual(address_url_detail, f'/api/addresses/{self.address_pk}/')

        response = self.client.get(address_url_detail)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # list
        response = self.client.get(address_url_list)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_address(self):
        self.test_create_address()

        address_url_detail = reverse('API:addresses-detail', kwargs={'pk': self.address_pk})

        self.assertEqual(address_url_detail, f'/api/addresses/{self.address_pk}/')

        data = {'street': 'Sienkiewicza'}

        response = self.client.patch(address_url_detail, data, format='json')

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_address(self):
        self.test_create_address()

        address_url_detail = reverse('API:addresses-detail', kwargs={'pk': self.address_pk})

        self.assertEqual(address_url_detail, f'/api/addresses/{self.address_pk}/')

        response = self.client.delete(address_url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIBookTestCase(APIGenreTestCase, APIPublisherTestCase, APIAuthorTestCase):
    book_pk = None

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_create_book(self):
        self.assertEqual(book_url_list, '/api/books/')

        self.test_create_author()
        self.test_create_genre()
        self.test_create_publisher()

        data = {'title': 'Krew elfów',
                'summary': '',
                'author': [self.author_pk],
                'publisher': self.publisher_pk,
                'amount': 20,
                'genre': [self.genre_pk],
                'number_of_pages': 250,
                'year_of_release': 1995}

        response = self.client.post(book_url_list, data, format='multipart')

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.book_pk = response.json()['id']

    def test_get_books(self):
        self.test_create_book()
        self.test_create_book()

        book_url_detail = reverse('API:books-detail', kwargs={'pk': self.book_pk})

        # retrieve
        self.assertEqual(book_url_detail, f'/api/books/{self.book_pk}/')

        response = self.client.get(book_url_detail)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # list
        response = self.client.get(book_url_list)

        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_book(self):
        self.test_create_book()

        book_url_detail = reverse('API:books-detail', kwargs={'pk': self.book_pk})

        self.assertEqual(book_url_detail, f'/api/books/{self.book_pk}/')

        data = {'amount': '120'}

        response = self.client.patch(book_url_detail, data, format='json')

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        self.test_create_book()

        book_url_detail = reverse('API:books-detail', kwargs={'pk': self.book_pk})

        self.assertEqual(book_url_detail, f'/api/books/{self.book_pk}/')

        response = self.client.delete(book_url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class APIOrderTestCase(APIBookTestCase, APIDelivererTestCase):
    order_pk = None

    def setUp(self):
        token = self.auth_user_test()
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_create_order(self):
        self.test_create_book()
        self.test_create_deliverer()

        book_url_detail = reverse('API:books-detail', kwargs={'pk': self.book_pk})

        book = self.client.get(book_url_detail)

        print(f"\n\nAmount before creating order: {book.json()['amount']}\n\n")

        data = {'book': [self.book_pk],
                'deliverer': self.deliverer_pk,
                'address': {
                    'street': 'Mickiewicza',
                    'number_of_building': '23',
                    'number_of_apartment': '',
                    'city': 'Lublin',
                    'state': 'lubelskie',
                    'zip_code': '23-100'
                    }
                }

        response = self.client.post(order_url_list, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #print(response.json())

        self.order_pk = response.json()['id']
        book = response.json()['book']

        print(f"\n\nAmount after creating order: {book[0]['amount']}\n\n")

    def test_get_orders(self):
        print('------------------c')
        self.test_create_order()
        self.test_create_order()

        order_url_detail = reverse('API:orders-detail', kwargs={'pk': self.order_pk})

        #retrieve
        response = self.client.get(order_url_detail)

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print('\n\n\n')

        #list
        response = self.client.get(order_url_list)

        #print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Update of order is impossible

    def test_delete_order(self):
        self.test_create_order()

        order_url_detail = reverse('API:orders-detail', kwargs={'pk': self.order_pk})
        book_url_detail = reverse('API:books-detail', kwargs={'pk': self.book_pk})

        book = self.client.get(book_url_detail)
        print(f"\n\nAmount before deleting order: {book.json()['amount']}\n\n")

        response = self.client.delete(order_url_detail)

        book = self.client.get(book_url_detail)
        print(f"\n\nAmount after deleting order: {book.json()['amount']}\n\n")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
'''

