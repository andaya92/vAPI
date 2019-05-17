# Generated by Django 2.0.3 on 2019-05-14 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20190514_0746'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventcity',
            name='zip_code',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.ZipCode'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zipcode',
            name='state',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.EventState'),
            preserve_default=False,
        ),
    ]
