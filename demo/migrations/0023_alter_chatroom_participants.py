# Generated by Django 4.2.16 on 2024-09-26 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0022_alter_chatroom_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='participants',
            field=models.ManyToManyField(related_name='chat_rooms', to='demo.profile'),
        ),
    ]
