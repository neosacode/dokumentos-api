from django.contrib import admin
from apps.documents.models import Country, Document, Model, Type

admin.site.register(Country)
admin.site.register(Document)
admin.site.register(Model)
admin.site.register(Type)
