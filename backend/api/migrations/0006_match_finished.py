# Generated by Django 3.1.7 on 2021-03-04 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210304_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
