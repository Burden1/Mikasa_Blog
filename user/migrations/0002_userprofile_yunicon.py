# Generated by Django 2.0.13 on 2022-06-13 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='yunicon',
            field=models.CharField(default='', max_length=200),
        ),
    ]