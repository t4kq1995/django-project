# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0004_administrator'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='theme',
            field=models.CharField(default=b'Theme', max_length=128),
        ),
    ]
