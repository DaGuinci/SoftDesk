# Generated by Django 4.2.4 on 2023-08-10 12:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_age_user_can_be_contacted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=18, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='can_be_contacted',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='can_data_be_shared',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
