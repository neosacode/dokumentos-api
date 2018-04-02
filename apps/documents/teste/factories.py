from apps.documents.models import Model, Type, Country, Document
from apps.core.tests import UserFactory
import factory


class TypeModelFactory(factory.django.DjangoModelFactory):

    name = 'identification'
    abbr = 'IDT'

    class Meta:
        model = Type
        django_get_or_create = ('abbr',)


class CountryModelFactory(factory.django.DjangoModelFactory):
    name = 'BRAZIL'
    abbr = 'BRL'

    class Meta:
        model = Country
        django_get_or_create = ('abbr',)


class ModelModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Model
    country = factory.SubFactory(CountryModelFactory)
    type = factory.SubFactory(TypeModelFactory)
    name = 'Carteira Nacional de Habilitação'
    abbr = 'CNH'


class DocumentModelFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Document

    country = factory.SubFactory(CountryModelFactory)
    type = factory.SubFactory(TypeModelFactory)
    model = factory.SubFactory(ModelModelFactory)
    user = factory.SubFactory(UserFactory)
