# Generated by Django 4.1.7 on 2023-04-07 17:11

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0010_rename_mypolygon_mpolygons'),
    ]

    operations = [
        migrations.CreateModel(
            name='myProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomp', models.CharField(max_length=50, null=True)),
                ('geomp', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]
