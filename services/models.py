from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self) -> str:
        return f"Service [{self.id}]"
