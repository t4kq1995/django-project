# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0005_message_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(default=b'N', max_length=1, choices=[(b'R', b'Read'), (b'N', b'Not read')]),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(default=b'N', max_length=1, choices=[(b'R', b'Read'), (b'N', b'Not read')]),
        ),
    ]
