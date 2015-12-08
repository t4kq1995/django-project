# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.CharField(default=b'index', max_length=64),
        ),
    ]
