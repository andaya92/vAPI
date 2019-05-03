# Generated by Django 2.0.3 on 2019-05-01 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20190430_2228'),
    ]

    operations = [
        migrations.CreateModel(
            name='VolunteerPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='empty_user_post.png', upload_to='user_posts')),
                ('caption', models.CharField(max_length=480)),
                ('created', models.DateTimeField(editable=False)),
                ('modified', models.DateTimeField()),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.VolunteerEvent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
