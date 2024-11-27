# Generated by Django 5.1.3 on 2024-11-22 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('auth_flow', '0018_alter_allusers_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allusers',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission'),
        ),
    ]
