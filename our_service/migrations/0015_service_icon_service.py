# Generated by Django 5.1.3 on 2024-12-09 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('our_service', '0014_serviceorderstep_data_user_file_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='icon_service',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
