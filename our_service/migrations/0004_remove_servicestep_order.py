# Generated by Django 5.1.3 on 2024-11-28 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('our_service', '0003_servicestep_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicestep',
            name='order',
        ),
    ]
