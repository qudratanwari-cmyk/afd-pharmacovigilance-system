from django.contrib import admin

from .models import ReporterType, HealthFacility, Reporter


@admin.register(ReporterType)
class ReporterTypeAdmin(admin.ModelAdmin):

    list_display = ("id", "reporter_type")

    search_fields = ("reporter_type",)


@admin.register(HealthFacility)
class HealthFacilityAdmin(admin.ModelAdmin):

    list_display = (
        "facility_name",
        "facility_type",
        "province",
        "phone_number",
    )

    list_filter = (
        "province",
        "facility_type",
    )

    search_fields = (
        "facility_name",
        "phone_number",
    )


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "reporter_type",
        "phone_number",
       
    )

    list_filter = (
        "reporter_type",
        
    )

    search_fields = (
        "full_name",
        "phone_number",
    )