# Generated by Django 4.0.4 on 2022-09-05 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='facebookId',
            new_name='facebook_id',
        ),
        migrations.RenameField(
            model_name='session',
            old_name='sessionId',
            new_name='session_id',
        ),
    ]