# Generated by Django 4.2 on 2025-03-29 09:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('closed_at', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('director', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dir_company', to=settings.AUTH_USER_MODEL, verbose_name='Директор')),
                ('employees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудники')),
            ],
            options={
                'verbose_name': 'Компания',
                'verbose_name_plural': 'Компании',
            },
        ),
        migrations.CreateModel(
            name='LegalDetailsCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='companies.company', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Юридические данные',
                'verbose_name_plural': 'Юридические данные',
            },
        ),
    ]
