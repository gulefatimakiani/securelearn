# Generated by Django 4.2.7 on 2023-12-01 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_rename_firstname_registeredusers_password1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutorialcomments',
            old_name='content',
            new_name='text',
        ),
    ]
