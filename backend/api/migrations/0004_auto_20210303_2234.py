# Generated by Django 3.1.7 on 2021-03-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210301_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='guest_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='match',
            name='host_score',
            field=models.IntegerField(default=0),
        ),
    ]
