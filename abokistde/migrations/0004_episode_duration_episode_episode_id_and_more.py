# Generated by Django 4.1.4 on 2023-01-29 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abokistde', '0003_rename_youtube_channel_id_publishingchannel_channel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='episode_id',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='published',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='updated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='episode',
            name='viewcount',
            field=models.IntegerField(null=True),
        ),
    ]
