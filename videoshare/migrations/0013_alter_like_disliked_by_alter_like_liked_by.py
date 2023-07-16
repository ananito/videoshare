# Generated by Django 4.2.2 on 2023-07-15 19:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videoshare", "0012_remove_like_dislikes_remove_like_likes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="like",
            name="disliked_by",
            field=models.ManyToManyField(
                blank=True, related_name="video_dislikes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="like",
            name="liked_by",
            field=models.ManyToManyField(
                blank=True, related_name="video_likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]