# Generated by Django 3.1.7 on 2021-03-13 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_video_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('code', models.CharField(max_length=20)),
            ],
        ),
    ]
