from django.contrib import admin
from .models import Country, Documents, Model, Type
# Register your models here.

admin.site.register(Country)
admin.site.register(Documents)
admin.site.register(Model)
admin.site.register(Type)
