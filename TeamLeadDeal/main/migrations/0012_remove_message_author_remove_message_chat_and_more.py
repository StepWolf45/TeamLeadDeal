# Generated by Django 4.1.4 on 2023-03-01 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_message_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='author',
        ),
        migrations.RemoveField(
            model_name='message',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='message',
            name='recipient',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
