# Generated by Django 4.2.16 on 2024-09-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0016_alter_trade_buyers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='buyers',
            field=models.CharField(choices=[('User', 'hzh'), ('User', 'oopq'), ('User', 'oopz'), ('', '---------')], default='', max_length=50),
        ),
    ]