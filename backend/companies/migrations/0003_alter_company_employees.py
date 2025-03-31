# Generated by Django 4.2 on 2025-03-29 12:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('companies', '0002_alter_company_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='employees',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудники'),
        ),
    ]
