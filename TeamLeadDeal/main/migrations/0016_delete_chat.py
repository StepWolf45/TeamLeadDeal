# Generated by Django 4.1.4 on 2023-03-01 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_message_chat'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Chat',
        ),
    ]