# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.TextField(max_length=1000, null=True, blank=True)),
                ('facebook_link', models.CharField(max_length=320, null=True, verbose_name=b'Facebook profile url', blank=True)),
                ('twitter_handle', models.CharField(max_length=320, null=True, verbose_name=b'Twitter handle url', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
