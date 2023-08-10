# Generated by Django 4.2.4 on 2023-08-10 12:20

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AddField(
            model_name='user',
            name='can_be_contacted',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='can_data_be_shared',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
