# Generated by Django 4.2.3 on 2023-07-25 18:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("videoshare", "0022_alter_commentlike_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="userviewhistory",
            name="date",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
