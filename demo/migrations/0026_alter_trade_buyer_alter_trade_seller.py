# Generated by Django 4.2.16 on 2024-09-30 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0025_alter_trade_buyer_alter_trade_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='buyer',
            field=models.CharField(choices=[('hzh', 'hzh'), ('oopq', 'oopq'), ('oopz', 'oopz'), ('', '---------')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='trade',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.profile'),
        ),
    ]
