# Generated by Django 4.0.6 on 2022-07-26 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_properties', '0002_order'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0009_alter_task_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_properties.order'),
        ),
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]