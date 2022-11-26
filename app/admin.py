from django.contrib import admin
from .models import Client, Service, Organisation, Bill

admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Organisation)
admin.site.register(Bill)
