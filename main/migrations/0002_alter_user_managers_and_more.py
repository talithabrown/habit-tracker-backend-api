# Generated by Django 4.1.5 on 2023-01-05 19:45

import datetime
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', main.models.CustomUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='habitcompletedate',
            name='complete_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]