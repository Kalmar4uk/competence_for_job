# Generated by Django 4.2 on 2025-03-30 07:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_alter_company_closed_at_alter_company_created_at_and_more'),
        ('users', '0011_user_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='companies.company', verbose_name='Компания'),
        ),
    ]
