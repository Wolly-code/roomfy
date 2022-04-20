# Generated by Django 4.0.2 on 2022-04-20 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=15)),
                ('phone_number', models.CharField(max_length=15)),
                ('occupation', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('pet_owner', models.BooleanField()),
                ('location', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('Budget', models.IntegerField()),
                ('Preference', models.CharField(max_length=25)),
                ('Title', models.CharField(max_length=25)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('photo1', models.ImageField(blank=True, upload_to='tenant')),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Tenant_Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourite', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenant.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report_Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='Scam', max_length=200)),
                ('Reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenant.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Payment_Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Payment_ID', models.CharField(max_length=50)),
                ('Amount', models.IntegerField()),
                ('Payment_date', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenant.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('Tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tenant.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
