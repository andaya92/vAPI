# Generated by Django 2.0.3 on 2019-05-21 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_auto_20190517_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteerevent',
            name='tags',
            field=models.CharField(default='{}', max_length=2000),
        ),
    ]
