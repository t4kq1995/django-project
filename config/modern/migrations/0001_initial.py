# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(default=b'Empty', max_length=128)),
                ('type', models.CharField(default=b'Info', max_length=1, choices=[(b'S', b'Success'), (b'D', b'Danger'), (b'I', b'Info')])),
                ('status', models.CharField(default=b'Not read', max_length=1, choices=[(b'R', b'Read'), (b'N', b'Not read')])),
                ('datetime', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
