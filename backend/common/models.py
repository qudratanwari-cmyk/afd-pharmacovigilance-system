from django.db import models


class Province(models.Model):
    province_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "provinces"
        ordering = ["province_name"]

    def __str__(self):
        return self.province_name


class Gender(models.Model):
     # Internal code used by business rules
    code = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )
    gender_name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "genders"

    def __str__(self):
        return self.gender_name


class Language(models.Model):
    language_name = models.CharField(max_length=50, unique=True)
    language_code = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "languages"

    def __str__(self):
        return self.language_name


class Setting(models.Model):
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    backup_frequency = models.CharField(max_length=30)

    email_enabled = models.BooleanField(default=True)

    sms_enabled = models.BooleanField(default=True)

    max_image_size_mb = models.IntegerField(default=5)

    max_pdf_size_mb = models.IntegerField(default=10)

    class Meta:
        db_table = "settings"

    def __str__(self):
        return f"System Settings ({self.language})"