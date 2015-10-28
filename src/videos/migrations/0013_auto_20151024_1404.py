# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_video_share_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='share_message',
            field=models.TextField(default=b'Check out this awesome video'),
        ),
    ]
