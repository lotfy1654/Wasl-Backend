# Generated by Django 5.1.3 on 2024-11-22 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_flow', '0022_alter_allusers_managers_remove_allusers_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allusers',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
