# Generated by Django 5.2.4 on 2025-07-20 11:40

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="contact",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, region=None
            ),
        ),
    ]
