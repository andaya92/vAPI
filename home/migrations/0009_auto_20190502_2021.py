# Generated by Django 2.0.3 on 2019-05-02 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20190502_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventcity',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.EventState'),
        ),
        migrations.AlterUniqueTogether(
            name='eventcity',
            unique_together={('name', 'state')},
        ),
    ]
