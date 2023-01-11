from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=10, unique=True,null=False, blank=False)
    description = models.CharField(max_length=100,null=False, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2,null=False, blank=False)

    def __repr__(self) -> str:
        return f"Service [{self.id}]"
