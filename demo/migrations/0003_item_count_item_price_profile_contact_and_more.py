# Generated by Django 4.2.16 on 2024-09-23 00:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_rename_skill_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='count',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MaxValueValidator(1000000.0), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MaxValueValidator(1000000.0), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='contact',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100000000000.0), django.core.validators.MinValueValidator(10000000000.0)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='dormitory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='facauty',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='student_class',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='student_id',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100000000000.0), django.core.validators.MinValueValidator(10000000000.0)]),
        ),
    ]