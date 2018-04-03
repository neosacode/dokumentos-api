from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from apps.documents import views
from django.contrib.auth import get_user_model
from apps.documents.teste.factories import (TypeModelFactory,
                                            ModelModelFactory,
                                            CountryModelFactory,
                                            )


class TestDocument(APITestCase):

    def setUp(self):
        self.view = views.DocumentViewSet.as_view({'get': 'list'})
        self.uri = '/documents/'
        self.user = self.setup_user()
        self.client = APIClient()
        self.country = CountryModelFactory()
        self.type = TypeModelFactory()
        self.model = ModelModelFactory()

    def setup_user(self):
        User = get_user_model()
        return User.objects.create_user(
            username='test',
            password="123456789",
            first_name='Fulano',
            last_name='de souza'
        )

    def test_list(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token.key)
        response = self.client.get(self.uri)
        self.assertEquals(response.status_code, 200,
                          'Expected Response Code 200, received {0} instead.'
                          .format(response.status_code))

    def test_create(self):
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token.key)
        params = {
                'file': 'http://meusite.com/arquivo.jpg',
                'webhook': 'http://meusite.com/',
                'type': self.type.abbr,
                'country': self.country.abbr,
                'model': self.model.abbr,
                'user': self.user,
                'status': 'pending',
                'ref': 'someref',
            }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))
