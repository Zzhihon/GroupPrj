# Generated by Django 4.2.16 on 2024-09-24 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0015_trade_buyers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='buyers',
            field=models.CharField(choices=[('User', 'hzh'), ('User', 'oopq'), ('User', 'oopz'), ('', 'default')], default='', max_length=50),
        ),
    ]
