# Generated by Django 2.2.4 on 2019-08-02 16:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250, verbose_name='Titel')),
                ('start', models.DateTimeField(verbose_name='Anfang')),
                ('end', models.DateTimeField(verbose_name='Ende')),
                ('description', models.TextField(blank=True, verbose_name='Beschreibung')),
                ('location', models.CharField(blank=True, max_length=250, verbose_name='Ort')),
            ],
        ),
    ]
