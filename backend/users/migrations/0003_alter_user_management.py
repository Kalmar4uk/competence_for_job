# Generated by Django 4.2 on 2024-11-28 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_jobdepartment_user_job_title_alter_user_middle_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='management',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.jobmanagement', verbose_name='Управление'),
        ),
    ]