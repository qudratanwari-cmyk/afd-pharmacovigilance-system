from django.db import models


class Manufacturer(models.Model):

    manufacturer_name = models.CharField(max_length=200)

    country = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "manufacturers"
        ordering = ["manufacturer_name"]

    def __str__(self):
        return self.manufacturer_name


class DrugType(models.Model):

    drug_type_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "drug_types"

    def __str__(self):
        return self.drug_type_name


class Drug(models.Model):

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name="drugs"
    )

    generic_name = models.CharField(max_length=200)

    brand_name = models.CharField(max_length=200, blank=True)

    dosage_form = models.CharField(max_length=100)

    strength = models.CharField(max_length=100)

    batch_number = models.CharField(max_length=100)

    manufacture_date = models.DateField(null=True, blank=True)

    expiry_date = models.DateField(null=True, blank=True)

    drug_image = models.ImageField(
        upload_to="drugs/",
        blank=True,
        null=True
    )

    class Meta:
        db_table = "drugs"

    def __str__(self):
        return self.generic_name