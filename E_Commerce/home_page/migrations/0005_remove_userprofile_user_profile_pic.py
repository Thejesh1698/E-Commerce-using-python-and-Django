# Generated by Django 3.0.5 on 2020-04-26 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0004_auto_20200424_1723'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_profile_pic',
        ),
    ]
