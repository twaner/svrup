# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0011_video_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='share_message',
            field=models.TextField(default=b'\nCHECK OUT THIS AWESOME VIDEO\n'),
        ),
    ]
