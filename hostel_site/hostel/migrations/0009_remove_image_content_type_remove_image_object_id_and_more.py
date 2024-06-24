# Generated by Django 5.0.4 on 2024-04-23 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0008_alter_image_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='image',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]