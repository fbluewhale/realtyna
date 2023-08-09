# Generated by Django 4.2.4 on 2023-08-08 20:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Room",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("number", models.IntegerField()),
                ("title", models.CharField(blank=True, default="", max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
