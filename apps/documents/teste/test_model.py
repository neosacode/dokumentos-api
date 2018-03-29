from django.test import TestCase
from apps.documents.models import Model, Type, Country, Document
from apps.documents.teste.factories import (TypeModelFactory,
                                            ModelModelFactory,
                                            CountryModelFactory,
                                            DocumentModelFactory
                                            )


class TypeModelTest(TestCase):

    def setUp(self):
        self.obj = TypeModelFactory()

    def test_create(self):
        self.assertTrue(Type.objects.exists())

    def test_str(self):
        self.assertEqual('identification', str(self.obj))


class ModelModelTest(TestCase):

    def setUp(self):
        self.obj = ModelModelFactory()

    def test_create(self):
        self.assertTrue(Model.objects.exists())

    def test_str(self):
        self.assertEqual('Carteira Nacional de Habilitação', str(self.obj))


class CountryModelTest(TestCase):

    def setUp(self):
        self.obj = CountryModelFactory()

    def test_create(self):
        self.assertTrue(Country.objects.exists())

    def test_str(self):
        self.assertEqual('BRAZIL', str(self.obj))


class DocumentModelTest(TestCase):

    def setUp(self):
        self.obj = DocumentModelFactory()

    def test_create(self):
        self.assertTrue(Document.objects.exists())
