# Generated by Django 4.2 on 2025-03-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_jobdepartment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refreshtoken',
            name='refresh_token',
            field=models.CharField(max_length=255, unique=True, verbose_name='Refresh Token'),
        ),
    ]
