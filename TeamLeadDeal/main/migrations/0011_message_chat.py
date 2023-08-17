# Generated by Django 4.1.4 on 2023-03-01 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_chats_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.chat', verbose_name='chat'),
            preserve_default=False,
        ),
    ]