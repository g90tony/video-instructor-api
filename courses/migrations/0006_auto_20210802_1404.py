# Generated by Django 3.2.4 on 2021-08-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredcourses',
            name='course',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='registeredcourses',
            name='profile',
            field=models.IntegerField(),
        ),
    ]