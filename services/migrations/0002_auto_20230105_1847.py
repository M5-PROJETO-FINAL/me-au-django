# Generated by Django 4.1.5 on 2023-01-05 21:47

from django.db import migrations


def populate_services(apps, schema_editor):
    data = [
        {
            "name": "Vacina",
            "description": "Vacinação para seu pet, com preço a combinar (dependendo de qual a vacina)",
            "price": 0,
        },
        {
            "name": "Banho",
            "description": "Banho para deixar o seu pet cheirosinho!",
            "price": 30,
        },
        {
            "name": "Tosa",
            "description": "Tosa completa para deixar seu pet no estilo",
            "price": 30,
        },
        {
            "name": "Massagem",
            "description": "Uma sessão relaxante de massagem",
            "price": 60,
        },
        {
            "name": "Natação",
            "description": "Aula de natação em uma piscina enorme e aquecida",
            "price": 50,
        },
        {
            "name": "Ração",
            "description": "Uma porção de ração premium gourmet",
            "price": 10,
        },
    ]
    Service = apps.get_model("services", "Service")
    for service_data in data:
        Service.objects.create(**service_data)


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [migrations.RunPython(populate_services)]
