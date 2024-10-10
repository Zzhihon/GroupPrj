# Generated by Django 4.2.16 on 2024-09-30 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0026_alter_trade_buyer_alter_trade_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='demo.profile'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='demo.profile'),
        ),
    ]
