# Generated by Django 4.2 on 2025-03-29 12:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_remove_company_director_remove_company_employees_and_more'),
        ('users', '0010_alter_user_is_director'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='companies.company', verbose_name='Компания'),
        ),
    ]
