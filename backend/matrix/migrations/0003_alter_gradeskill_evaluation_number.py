# Generated by Django 4.2 on 2024-12-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrix', '0002_gradeskill_evaluation_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gradeskill',
            name='evaluation_number',
            field=models.PositiveSmallIntegerField(verbose_name='Числовая оценка'),
        ),
    ]
