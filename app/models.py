from django.core.validators import MinValueValidator
from django.db import models


class Organisation(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Service(models.Model):
    name = models.CharField(max_length=500, unique=True)


class Bill(models.Model):
    client = models.ForeignKey(
        "Client", on_delete=models.PROTECT, related_name="client_bill"
    )
    organisation = models.ForeignKey(
        "Organisation", on_delete=models.PROTECT, related_name="org_bill"
    )
    bill_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    summa = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateField()
    service = models.ForeignKey(
        "Service", on_delete=models.PROTECT, related_name="serivice_bill"
    )

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
        ordering = ["-date"]
        constraints = [
            models.UniqueConstraint(
                fields=["client", "organisation", "bill_number"],
                name="client_org_number need to be unique",
            )
        ]
