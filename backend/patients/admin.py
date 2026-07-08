from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "medical_record_no",
        "gender",
        "age",
        "province",
    )

    list_filter = (
        "gender",
        "province",
    )

    search_fields = (
        "full_name",
        "medical_record_no",
        "phone_number",
    )