# Generated by Django 4.1.5 on 2023-02-09 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abokistde', '0012_remove_provider_technical_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='display_name',
            new_name='name',
        ),
    ]