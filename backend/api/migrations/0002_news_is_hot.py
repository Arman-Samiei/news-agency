# Generated by Django 3.1.7 on 2021-02-27 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='is_hot',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
