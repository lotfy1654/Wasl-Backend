# Generated by Django 5.1.3 on 2024-12-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_flow', '0029_allusers_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='allusers',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='allusers',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
