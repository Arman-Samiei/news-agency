# Generated by Django 3.1.7 on 2021-03-24 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_confirmationcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirmationcode',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
