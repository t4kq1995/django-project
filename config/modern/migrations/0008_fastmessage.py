# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modern', '0007_auto_20151016_0707'),
    ]

    operations = [
        migrations.CreateModel(
            name='FastMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('user_receive', models.ForeignKey(related_name='user_receive', to=settings.AUTH_USER_MODEL)),
                ('user_send', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
