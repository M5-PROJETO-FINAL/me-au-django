from django.db import models


class Service(models.Model):
    name = models.CharField(unique=True)
    description = models.CharField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self) -> str:
        return f"Service [{self.id}]"

