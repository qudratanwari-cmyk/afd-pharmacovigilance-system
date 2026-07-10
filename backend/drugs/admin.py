from django.contrib import admin

from .models import (
    Manufacturer,
    DrugType,
    Drug,
)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):

    list_display = (
        "manufacturer_name",
        "country",
    )

    search_fields = (
        "manufacturer_name",
    )


@admin.register(DrugType)
class DrugTypeAdmin(admin.ModelAdmin):

    list_display = (
        "drug_type_name",
    )


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):

    list_display = (
        "generic_name",
        "brand_name",
        "manufacturer",
        "strength",
    )

    search_fields = (
        "generic_name",
        "brand_name",
    )

    list_filter = (
        "manufacturer",
    )