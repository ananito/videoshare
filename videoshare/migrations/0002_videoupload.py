# Generated by Django 4.2.2 on 2023-07-10 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("videoshare", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VideoUpload",
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
                (
                    "unique_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True, null=True)),
                ("video", models.FileField(upload_to="media/uploads/videos/")),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True, null=True, upload_to="media/uploads/images/"
                    ),
                ),
                ("public", models.BooleanField(default=True, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
