# Generated by Django 3.1.7 on 2021-08-14 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20210810_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rsslinks',
            name='rss_link',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]