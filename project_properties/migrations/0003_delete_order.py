# Generated by Django 4.0.6 on 2022-07-26 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_alter_project_order'),
        ('project_properties', '0002_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
