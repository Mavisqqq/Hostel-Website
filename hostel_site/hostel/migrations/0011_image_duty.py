# Generated by Django 5.0.4 on 2024-04-23 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0010_remove_image_duty'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='duty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hostel.duty', verbose_name='Дежурство'),
        ),
    ]
