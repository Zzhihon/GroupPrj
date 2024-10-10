# Generated by Django 4.2.16 on 2024-09-30 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0027_alter_trade_buyer_alter_trade_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chatRoom',
        ),
        migrations.AddField(
            model_name='message',
            name='trade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='demo.trade'),
        ),
    ]
