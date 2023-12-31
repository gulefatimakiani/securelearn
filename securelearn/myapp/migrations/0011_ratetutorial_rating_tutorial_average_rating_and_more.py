# Generated by Django 4.2.7 on 2023-12-08 05:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0010_ratetutorial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratetutorial',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=0),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='average_rating',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
        ),
        migrations.AlterUniqueTogether(
            name='ratetutorial',
            unique_together={('tutorial', 'user')},
        ),
        migrations.RemoveField(
            model_name='ratetutorial',
            name='score',
        ),
    ]
