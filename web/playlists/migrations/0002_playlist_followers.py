# Generated by Django 4.1.7 on 2023-04-07 08:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("playlists", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="playlist",
            name="followers",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
