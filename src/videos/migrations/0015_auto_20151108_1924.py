# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0014_taggeditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.SlugField(choices=[(b'python', b'python'), (b'django', b'django'), (b'css', b'css'), (b'bootstrap', b'bootstrap')]),
        ),
    ]
