# Generated by Django 5.1.3 on 2024-12-21 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_service', '0019_alter_service_icon_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorderstep',
            name='step_description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='servicestep',
            name='step_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
