# Generated by Django 5.1.3 on 2024-12-05 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0007_socialmedia_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whychooseus',
            name='icons_img',
        ),
        migrations.AddField(
            model_name='whychooseus',
            name='icons',
            field=models.TextField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
