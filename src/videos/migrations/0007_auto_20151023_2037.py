# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20151023_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='videos',
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ForeignKey(to='videos.Category', null=True),
        ),
    ]
