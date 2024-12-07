# Generated by Django 4.2 on 2024-12-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_jobdepartment_children_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobdepartment',
            options={'verbose_name': 'Департамент', 'verbose_name_plural': 'Департамент'},
        ),
        migrations.AlterModelOptions(
            name='jobgroup',
            options={'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='jobmanagement',
            options={'verbose_name': 'Управление', 'verbose_name_plural': 'Управление'},
        ),
        migrations.AddField(
            model_name='jobdepartment',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobgroup',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jobmanagement',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
