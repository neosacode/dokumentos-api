from django.contrib import admin
from .models import Country, Document, Model, Type
# Register your models here.

admin.site.register(Country)
admin.site.register(Document)
admin.site.register(Model)
admin.site.register(Type)
