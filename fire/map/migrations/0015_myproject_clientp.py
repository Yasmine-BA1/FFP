# Generated by Django 4.1.7 on 2023-04-07 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0006_client_supervisor_supervisor_supervisor_id'),
        ('map', '0014_myproject_locationp'),
    ]

    operations = [
        migrations.AddField(
            model_name='myproject',
            name='clientp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='signup.client'),
        ),
    ]
