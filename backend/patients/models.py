from django.db import models

from common.models import Province, Gender
from reporters.models import HealthFacility


class Patient(models.Model):

    health_facility = models.ForeignKey(
        HealthFacility,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT
    )

    gender = models.ForeignKey(
        Gender,
        on_delete=models.PROTECT
    )

    medical_record_no = models.CharField(
        max_length=100,
        blank=True
    )

    full_name = models.CharField(max_length=150)

    age = models.PositiveIntegerField()

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    is_pregnant = models.BooleanField(
        default=False
    )

    is_breast_feeding = models.BooleanField(
        default=False
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    class Meta:
        db_table = "patients"

    def __str__(self):
        return self.full_name