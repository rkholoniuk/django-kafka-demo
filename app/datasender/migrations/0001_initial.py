# Generated by Django 4.2.10 on 2024-02-28 19:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stamp",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_cid", models.CharField(max_length=255, unique=True)),
                (
                    "time_tolerance",
                    models.IntegerField(help_text="Time tolerance in minutes"),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        help_text="created_date datetime",
                    ),
                ),
            ],
        ),
    ]