from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='assets/images/profiles',
                               max_length=128,
                               default='assets/images/profiles/user.png')
    online = models.DateTimeField()

    def __str__(self):
        return 'User : {0}'.format(self.user.username)


class Administrator(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='assets/images/profiles',
                               max_length=128,
                               default='assets/images/profiles/user.png')
    online = models.DateTimeField()

    def __str__(self):
        return 'User : {0}'.format(self.user.username)


class Message(models.Model):
    READABLE = (
        ('R', 'Read'),
        ('N', 'Not read'),
        ('Z', 'Notes'),
        ('S', 'Spam'),
        ('T', 'Trash'),
    )
    IMPORTANT = (
        ('I', 'Important'),
        ('U', 'Unimportant'),
    )
    user_send = models.ForeignKey(User)
    user_receive = models.ForeignKey(User, related_name='user_received')
    theme = models.CharField(max_length=128, default='Theme')
    message = models.TextField()
    status = models.CharField(max_length=1, choices=READABLE, default='N')
    importance = models.CharField(max_length=1, choices=IMPORTANT, default='U')
    datetime = models.DateTimeField()

    def __str__(self):
        return 'Message from {0} to {1}({2})'.format(self.user_send, self.user_receive, self.status)


class Notification(models.Model):
    READABLE = (
        ('R', 'Read'),
        ('N', 'Not read'),
    )
    TYPE = (
        ('S', 'Success'),
        ('D', 'Danger'),
        ('I', 'Info'),
    )
    user = models.ForeignKey(User)
    message = models.CharField(max_length=128, default='Empty')
    type = models.CharField(max_length=1, choices=TYPE, default='Info')
    status = models.CharField(max_length=1, choices=READABLE, default='N')
    link = models.CharField(max_length=64, default='index')
    datetime = models.DateTimeField()

    def __str__(self):
        return 'Notification to {0} ({1}) '.format(self.user.username, self.status)


class FastMessage(models.Model):
    user_send = models.ForeignKey(User)
    user_receive = models.ForeignKey(User, related_name='user_receive')
    message = models.TextField()

    def __str__(self):
        return 'Message form {0} to {1}'.format(self.user_send.username, self.user_receive.username)
