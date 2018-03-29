from apps.documents.models import Model, Type, Country, Document
from apps.core.tests import UserFactory
import factory


class TypeModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Type

    name = 'identification'
    abbr = 'IDT'


class ModelModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Model

    name = 'Carteira Nacional de Habilitação'
    abbr = 'CNH'


class CountryModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Country

    name = 'BRAZIL'
    abbr = 'BRL'


class DocumentModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Document

    country = factory.SubFactory(CountryModelFactory)
    type = factory.SubFactory(TypeModelFactory)
    model = factory.SubFactory(ModelModelFactory)
    user = factory.SubFactory(UserFactory)
