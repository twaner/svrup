# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20151018_0007'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='featured',
            field=models.BooleanField(default=True),
        ),
    ]
