# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20151023_2006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='videos',
            field=models.ManyToManyField(to='videos.Video', null=True, blank=True),
        ),
    ]
