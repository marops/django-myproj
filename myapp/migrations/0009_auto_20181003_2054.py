# Generated by Django 2.0.6 on 2018-10-03 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20181003_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
