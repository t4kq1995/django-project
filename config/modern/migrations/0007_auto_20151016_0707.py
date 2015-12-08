# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modern', '0006_auto_20151015_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='importance',
            field=models.CharField(default=b'U', max_length=1, choices=[(b'I', b'Important'), (b'U', b'Unimportant')]),
        ),
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(default=b'N', max_length=1, choices=[(b'R', b'Read'), (b'N', b'Not read'), (b'Z', b'Notes'), (b'S', b'Spam'), (b'T', b'Trash')]),
        ),
    ]
