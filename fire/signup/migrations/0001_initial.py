# Generated by Django 4.1.7 on 2023-03-26 15:40

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('prenom', models.CharField(max_length=100, null=True)),
                ('NB_GSM', models.CharField(max_length=100, null=True)),
                ('pseudo', models.CharField(max_length=100, null=True)),
                ('e_mail', models.EmailField(max_length=100, null=True)),
                ('position', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='supervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, null=True)),
                ('prenom', models.CharField(max_length=100, null=True)),
                ('NB_GSM', models.CharField(max_length=100, null=True)),
                ('pseudo', models.CharField(max_length=100, null=True)),
                ('e_mail', models.EmailField(max_length=100, null=True)),
                ('position', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('image', models.ImageField(null=True, upload_to='')),
            ],
        ),
    ]
