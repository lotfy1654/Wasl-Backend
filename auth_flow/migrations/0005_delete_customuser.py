# Generated by Django 5.1.3 on 2024-11-20 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_flow', '0004_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
