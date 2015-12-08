__author__ = 't4kq'

"""
modern URL Configuration
"""
from django.conf.urls import url, include
# Basic
from modern import views
# Login
from modern.view import index
# Registration
from modern.view.unregistred import signup
# Authenticated
from modern.view.registred.user import userview
# Errors
from modern.view.errors import error
# Rest
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', userview.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    url(r'^$', views.check_authenticated, name='check'),

    # No authenticated
    url(r'^login$', index.LoginView.as_view(), name='login'),

    # Registration
    url(r'^signup$', signup.SignUp.as_view(), name='signup'),
    url(r'^forgot$', signup.ForgotPassword.as_view(), name='forgot'),

    # Authenticated / User
    url(r'^index$', userview.IndexView.as_view(), name='index'),

    # Messages
    url(r'^profile/messages$', userview.AllMessageView.as_view(), name='messages'),
    url(r'^profile/messages/send$', userview.MessageSendView.as_view(), name='message-send'),
    url(r'^profile/messages/spam$', userview.MessageSpamView.as_view(), name='message-spam'),
    url(r'^profile/messages/trash$', userview.MessageTrashView.as_view(), name='message-trash'),
    url(r'^profile/messages/send/(?P<message_id>[0-9]+)$', userview.SendDetailView.as_view(), name='message-send'),
    url(r'^profile/messages/(?P<message_id>[0-9]+)$', userview.MessageView.as_view(), name='message-view'),
    url(r'^profile/write$', userview.MessageWriteView.as_view(), name='message-write'),

    url(r'^logout$', userview.user_logout, name='logout'),

    # Errors
    url(r'^error/500$', error.Error500.as_view(), name='500'),
    url(r'^error/404$', error.Error404.as_view(), name='404'),

    # Rest
    url(r'^route/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
