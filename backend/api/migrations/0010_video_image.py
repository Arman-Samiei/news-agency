# Generated by Django 3.1.7 on 2021-03-09 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_match_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='image',
            field=models.ImageField(default=1, upload_to='Videos_image'),
            preserve_default=False,
        ),
    ]
