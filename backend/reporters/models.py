from django.db import models

from common.models import Province


class ReporterType(models.Model):

    # Internal code used by business rules
    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    reporter_type = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "reporter_types"

    def __str__(self):
        return self.reporter_type


class HealthFacility(models.Model):
    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="health_facilities"
    )

    facility_name = models.CharField(max_length=200)

    facility_type = models.CharField(max_length=100, blank=True)

    address = models.TextField(blank=True)

    phone_number = models.CharField(max_length=20, blank=True)

    email = models.EmailField(blank=True)

    class Meta:
        db_table = "health_facilities"

    def __str__(self):
        return self.facility_name


class Reporter(models.Model):

    reporter_type = models.ForeignKey(
        ReporterType,
        on_delete=models.PROTECT
    )

    health_facility = models.ForeignKey(
        HealthFacility,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    full_name = models.CharField(max_length=150)

    organization_name = models.CharField(
        max_length=200,
        blank=True
    )

    job_title = models.CharField(
        max_length=150,
        blank=True
    )

    phone_number = models.CharField(max_length=20)

    email = models.EmailField(
        blank=True,
        null=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    address = models.TextField(blank=True)

    stamp_image = models.ImageField(
        upload_to="stamps/",
        blank=True,
        null=True
    )

    registration_date = models.DateField()

    class Meta:
        db_table = "reporters"

    def __str__(self):
        return self.full_name