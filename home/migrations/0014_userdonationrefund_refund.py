# Generated by Django 2.0.3 on 2019-05-07 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_userdonationrefund'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdonationrefund',
            name='refund',
            field=models.CharField(default='abc', max_length=50),
            preserve_default=False,
        ),
    ]
