from django.contrib import admin
from .models import *

admin.site.register(Manufacturer)
admin.site.register(DrugType)
admin.site.register(Drug)