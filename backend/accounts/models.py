from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    role_name = models.CharField(
        max_length=50,
        unique=True
    )

    class Meta:
        db_table = "roles"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["role_name"]

    def __str__(self):
        return self.role_name


class User(AbstractUser):

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="users"
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_admin(self):
        """
        Check whether the user is an administrator.
        """
        return (
            self.role is not None
            and self.role.role_name == "Admin"
        )


    @property
    def is_reviewer(self):
        """
        Check whether the user is a reviewer.
        """
        return (
            self.role is not None
            and self.role.role_name == "Reviewer"
        )


    @property
    def is_reporter(self):
        """
        Check whether the user is a reporter.
        """
        return (
            self.role is not None
            and self.role.role_name == "Reporter"
        )

    class Meta:
        db_table = "users"

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username