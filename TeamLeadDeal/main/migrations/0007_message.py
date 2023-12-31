# Generated by Django 4.1.5 on 2023-03-01 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_worksheet_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=160)),
                ('author_id', models.IntegerField()),
                ('recipient_id', models.IntegerField()),
                ('is_checked', models.BooleanField(default=False)),
                ('date', models.DateField()),
            ],
        ),
    ]
