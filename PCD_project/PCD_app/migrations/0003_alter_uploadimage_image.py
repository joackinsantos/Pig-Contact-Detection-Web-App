# Generated by Django 4.1.7 on 2023-05-10 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("PCD_app", "0002_uploadimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploadimage",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="pig-images/"),
        ),
    ]
