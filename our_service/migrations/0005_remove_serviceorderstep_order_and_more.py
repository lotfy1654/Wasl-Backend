# Generated by Django 5.1.3 on 2024-11-28 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('our_service', '0004_remove_servicestep_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorderstep',
            name='order',
        ),
        migrations.RemoveField(
            model_name='serviceorderstep',
            name='step',
        ),
        migrations.DeleteModel(
            name='ServiceOrder',
        ),
        migrations.DeleteModel(
            name='ServiceOrderStep',
        ),
    ]
