# Generated by Django 5.0.4 on 2024-04-14 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0003_remove_messages_chat_remove_block_chat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='block',
        ),
        migrations.AddField(
            model_name='block',
            name='messages',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hostel.messages', verbose_name='Сообщения'),
        ),
    ]
