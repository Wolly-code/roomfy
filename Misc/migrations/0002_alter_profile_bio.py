# Generated by Django 4.0.2 on 2022-04-24 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Misc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(max_length=200),
        ),
    ]
