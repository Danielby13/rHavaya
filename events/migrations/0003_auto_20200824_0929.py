# Generated by Django 3.1 on 2020-08-24 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_events_event_hour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='geolocation',
        ),
        migrations.AddField(
            model_name='events',
            name='google_map',
            field=models.CharField(default='', max_length=255),
        ),
    ]
