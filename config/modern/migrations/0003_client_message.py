# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modern', '0002_notification_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(default=b'assets/images/profiles/user.png', max_length=128, upload_to=b'assets/images/profiles')),
                ('online', models.DateTimeField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('status', models.CharField(default=b'Not read', max_length=1, choices=[(b'R', b'Read'), (b'N', b'Not read')])),
                ('datetime', models.DateTimeField()),
                ('user_receive', models.ForeignKey(related_name='user_received', to=settings.AUTH_USER_MODEL)),
                ('user_send', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
