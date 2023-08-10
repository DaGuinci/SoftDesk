# Generated by Django 4.2.4 on 2023-08-10 12:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_age_alter_user_can_be_contacted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(120)]),
        ),
        migrations.AlterField(
            model_name='user',
            name='can_be_contacted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='can_data_be_shared',
            field=models.BooleanField(default=False),
        ),
    ]
