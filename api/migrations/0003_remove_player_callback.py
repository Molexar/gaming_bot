# Generated by Django 4.0.4 on 2022-04-26 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_player_callback_alter_player_game'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='callback',
        ),
    ]
