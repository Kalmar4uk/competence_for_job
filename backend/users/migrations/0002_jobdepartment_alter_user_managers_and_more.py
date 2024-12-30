# Generated by Django 4.2 on 2024-12-21 09:47

import django.db.models.deletion
from django.db import migrations, models

import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('is_delete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Департамент',
                'verbose_name_plural': 'Департамент',
            },
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='job_title',
            field=models.CharField(max_length=50, null=True, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='personnel_number',
            field=models.CharField(max_length=8, null=True, unique=True, validators=[users.validators.validation_min_length_personnal_number], verbose_name='Табельный номер'),
        ),
        migrations.CreateModel(
            name='JobManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('is_delete', models.BooleanField(default=False)),
                ('children', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobdepartment', verbose_name='Департамент')),
            ],
            options={
                'verbose_name': 'Управление',
                'verbose_name_plural': 'Управление',
            },
        ),
        migrations.CreateModel(
            name='JobGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('is_delete', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobdepartment')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.AddField(
            model_name='jobdepartment',
            name='children',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobgroup', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='jobdepartment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.jobmanagement', verbose_name='Управление'),
        ),
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.jobdepartment', verbose_name='Департамент'),
        ),
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.jobgroup', verbose_name='Группа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='management',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.jobmanagement', verbose_name='Управление'),
        ),
    ]
