# Generated by Django 4.2.16 on 2024-09-23 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0005_remove_review_trade_trade_review_alter_trade_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trade',
            old_name='owner',
            new_name='seller',
        ),
    ]
