# Generated by Django 3.2.5 on 2021-07-16 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tracks_qty',
            field=models.IntegerField(default=0),
        ),
    ]
