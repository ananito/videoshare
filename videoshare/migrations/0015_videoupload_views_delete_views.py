# Generated by Django 4.2.3 on 2023-07-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("videoshare", "0014_views_userviewhistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="videoupload",
            name="views",
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name="Views",
        ),
    ]