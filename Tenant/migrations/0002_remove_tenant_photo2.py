# Generated by Django 4.0.2 on 2022-03-13 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tenant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenant',
            name='photo2',
        ),
    ]
