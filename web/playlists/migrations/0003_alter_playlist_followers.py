# Generated by Django 4.1.13 on 2023-12-10 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0002_playlist_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='followers',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
