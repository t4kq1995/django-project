from django.contrib import admin
from modern.models import Notification, Client, Administrator, Message, FastMessage

admin.site.register(Notification)
admin.site.register(Client)
admin.site.register(Administrator)
admin.site.register(Message)
admin.site.register(FastMessage)
