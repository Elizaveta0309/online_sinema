# Generated by Django 4.2.2 on 2023-06-11 10:24

import uuid

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models
from typing import List, Any


class Migration(migrations.Migration):

    initial = True

    dependencies: List[Any] = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.SlugField(max_length=255, verbose_name='name')),
                ('config_value', models.CharField(max_length=255, verbose_name='value')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('channel', models.CharField(choices=[('email', 'Email'), ('websocket', 'Websocket')], max_length=50)),
                ('subject', models.TextField(blank=True)),
                ('template', tinymce.models.HTMLField()),
                ('event', models.CharField(choices=[('review-reporting.v1.rated', 'Review Rated'), ('user-reporting.v1.registered', 'User Registered'), ('admin-reporting.v1.event', 'Admin')], max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScheduleMail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('template_params', models.TextField(blank=True, verbose_name='template_params')),
                ('user_group', models.CharField(choices=[('all', 'All')], max_length=50)),
                ('is_instant', models.BooleanField()),
                ('next_planned', models.DateTimeField(blank=True, null=True)),
                ('frequency', models.CharField(choices=[('once', 'Once'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], max_length=50)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('high', 'High')], max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('last_processed_date', models.DateTimeField(blank=True, null=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.template')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]