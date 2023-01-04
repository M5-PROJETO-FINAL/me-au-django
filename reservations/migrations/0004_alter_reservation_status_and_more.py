# Generated by Django 4.1.5 on 2023-01-04 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0003_reservationpet_pet_reservationpet_room_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="status",
            field=models.CharField(
                choices=[
                    ("reserved", "Reserved"),
                    ("active", "Active"),
                    ("concluded", "Concluded"),
                    ("cancelled", "Cancelled"),
                ],
                default="reserved",
                max_length=9,
            ),
        ),
        migrations.AlterField(
            model_name="reservationpet",
            name="reservation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservation_pets",
                to="reservations.reservation",
            ),
        ),
        migrations.AlterField(
            model_name="reservationservice",
            name="reservation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservation_services",
                to="reservations.reservation",
            ),
        ),
    ]
