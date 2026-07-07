from django.contrib import admin

from .models import ReporterType, HealthFacility, Reporter

admin.site.register(ReporterType)
admin.site.register(HealthFacility)
admin.site.register(Reporter)