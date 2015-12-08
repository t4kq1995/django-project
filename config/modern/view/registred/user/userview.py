# -*- coding: utf-8 -*-
__author__ = 't4kq'
from django.views.generic.base import TemplateView
from rest_framework import viewsets
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from modern.models import Notification, Client, Administrator, Message, FastMessage
from django.contrib.auth.models import User
from modern.serializers import UserSerializer
from django.db.models import Q, Count
from django.utils.safestring import mark_safe
import datetime
import os


class BaseDir(object):

    def __init__(self):
        pass

    # Different between two times
    @staticmethod
    def different(start_time, end):
        a, b, c, d = start_time.hour, start_time.minute, start_time.second, start_time.microsecond
        w, x, y, z = end.hour, end.minute, end.second, end.microsecond
        delta = (w-a)*60 + (x-b) + (y-c)/60. + (z-d)/60000000.
        if delta < 0:
            delta += 1440
        hh, rem = divmod(delta, 60)
        hh = int(hh)
        mm = int(rem)
        result = '%s %s'
        return result % (hh, mm)

    # Make correct datetime
    def correct_time(self, note):
        date_start = str(note).split(' ')[0]
        date_end = str(datetime.datetime.now()).split(' ')[0]

        ds = date_start.split('-')
        de = date_end.split('-')

        date_start = datetime.date(int(ds[0]), int(ds[1]), int(ds[2]))
        date_end = datetime.date(int(de[0]), int(de[1]), int(de[2]))

        answer = date_end - date_start
        ask = '%s %s'
        try:
            key = int(str(answer).split()[0])
        except ValueError:
            time_start = str(note).split(' ')[1]
            hour_start = time_start.split(':')[0]
            minute_start = time_start.split(':')[1]

            hour_end = str(datetime.datetime.now().time()).split(':')[0]
            minute_end = str(datetime.datetime.now().time()).split(':')[1]

            answer = self.different(datetime.time(int(hour_start), int(minute_start), 0),
                                    datetime.time(int(hour_end), int(minute_end), 0))

            hour = int(answer.split(' ')[0])
            minute = int(answer.split(' ')[1])
            if hour == 0:
                if minute == 0:
                    minute = 1
                return ask % (minute, 'мин.')
            else:
                return ask % (hour, 'час.')
        else:
            return ask % (key, 'дн.')

    # Make correct information
    @staticmethod
    def make_notification(count, str0, str1, str2):
        term = ''
        number = str(count)[1:]
        if number != '':
            number = int(number)
            if number > 10:
                if number < 15:
                    term = str0
        else:
            if count == 0 or count > 4:
                term = str0
            elif count == 1:
                term = str1
            elif count > 1:
                term = str2
        return 'У Вас ' + str(count) + ' ' + term

    def get_data(self, request):
        user = request.request.user
        context = {}

        # make online user
        if hasattr(user, 'client'):
            client = Client.objects.get(user=user)
            client.online = datetime.datetime.now()
            client.save()

            # show avatar info
            context['avatar'] = client
            context['position'] = 'Пользователь'
            profile = user.client

        elif hasattr(user, 'administrator'):
            admin = Administrator.objects.get(user=user)
            admin.online = datetime.datetime.now()
            admin.save()

            # show avatar info
            context['avatar'] = admin
            context['position'] = 'Администратор'
            profile = user.administrator

        # show unread messages
        context['message'] = Message.objects.filter(user_receive=user).filter(status='N')
        if context['message']:
            context['message_top'] = self.make_notification(len(context['message']), 'новых сообщений',
                                                            'новое сообщение', 'новых сообщения')
            for mess in context['message']:
                mess.datetime = self.correct_time(mess.datetime)
                # make online
                if hasattr(mess.user_send, 'client'):
                    online = self.correct_time(mess.user_send.client.online)
                    mess.avatar = mess.user_send.client.avatar
                elif hasattr(mess.user_send, 'administrator'):
                    online = self.correct_time(mess.user_send.administrator.online)
                    mess.avatar = mess.user_send.administrator.avatar
                if online.split(' ')[1] != 'мин.':
                    mess.online_user = False
                else:
                    if int(online.split(' ')[0]) > 15:
                        mess.online_user = False
                    else:
                        mess.online_user = True

        # show unread notification
        context['notification'] = Notification.objects.filter(user=user).filter(status='N')
        if context['notification']:
            context['notification_top'] = self.make_notification(len(context['notification']), 'новых уведомлений',
                                                                 'новое уведомление', 'новых уведомления')
            for note in context['notification']:
                note.datetime = self.correct_time(note.datetime)
                note.link = os.path.join(note.link)

        return context


class IndexView(TemplateView):
    template_name = 'auth/user/pages/main_page.html'

    @staticmethod
    def post(request):
        if request.is_ajax():
            if request.POST['key'] == 'note':
                note = Notification.objects.get(Q(user=request.user), Q(id=request.POST['id']))
                note.status = 'R'
                note.save()
                return JsonResponse({'success': True})
            elif request.POST['key'] == 'all_note':
                notes = Notification.objects.filter(user=request.user)
                all_note = []
                for note in notes:
                    local = {
                        'message': note.message,
                        'datetime': str(note.datetime).split(' ')[0],
                        'link': note.link,
                        'type': note.type
                    }
                    all_note.append(local)
                return JsonResponse({'notes': all_note})
            elif request.POST['key'] == 'message':
                return JsonResponse({'status': 'qq'})

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        array_users = []
        admins = Administrator.objects.all()
        clients = Client.objects.all()
        for admin in admins:
            array_users.append({'name': admin.user.first_name,
                                'surname': admin.user.last_name,
                                'login': admin.user.username,
                                'date_login': admin.online,
                                'status': 'Администратор'})

        for client in clients:
            array_users.append({'name': client.user.first_name,
                                'surname': client.user.last_name,
                                'login': client.user.username,
                                'date_login': client.online,
                                'status': 'Пользователь'})

        f_messages = []
        top_message = []
        user_send = []
        messages = FastMessage.objects.filter(user_receive=self.request.user)
        for message in messages:
            if message.user_send not in user_send:
                user_send.append(message.user_send)

        for user in user_send:
            list_messages = self.make_list_message(user, self.request.user)
            top_message.append(list_messages[0])
            f_messages.append(list_messages[1])

        context['top_message'] = top_message
        context['messages'] = f_messages
        # List of users
        context['users'] = array_users
        return context

    @staticmethod
    def make_list_message(sender, receiver):
        first_step = []
        second_step = []
        result = []
        messages = FastMessage.objects.filter(Q(user_send=sender) & Q(user_receive=receiver) |
                                              Q(user_send=receiver) & Q(user_receive=sender)).order_by('id')

        i = 0
        for message in messages:
            i += 1
            second_step.append({'username': sender.first_name + ' ' + sender.last_name,
                                'status': '1' if message.user_send == sender else '2',
                                'image': sender.client.avatar.url if hasattr(sender, 'client')
                                else sender.administrator.avatar.url,
                                'message': message.message})
            if i == len(messages):
                first_step.append({'username': sender.first_name + ' ' + sender.last_name,
                                   'image': sender.client.avatar.url if hasattr(sender, 'client')
                                   else sender.administrator.avatar.url,
                                   'message': message.message,
                                   'id': message.id})
        result.append(first_step)
        result.append(second_step)
        return result


class MessageView(TemplateView):
    template_name = 'auth/user/message/message-detail.html'

    @staticmethod
    def post(request, message_id):
        if request.is_ajax():
            if request.POST['key'] == 'message':
                message = Message.objects.get(Q(user_receive=request.user), Q(id=request.POST['id']))
                message.status = 'R'
                message.save()
                return JsonResponse({'success': True})

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        # form detail information
        try:
            message = Message.objects.get(Q(user_receive=self.request.user),
                                          Q(id=kwargs['message_id']))
        except Message.DoesNotExist:
            raise PermissionDenied

        message.status = 'R'
        message.save()

        message.datetime = str(message.datetime).split(' ')[0]
        if hasattr(message.user_send, 'client'):
            context['detail_mess_avatar'] = message.user_send.client.avatar
        elif hasattr(message.user_send, 'administrator'):
            context['detail_mess_avatar'] = message.user_send.administrator.avatar
        context['detail_mess_url'] = reverse('message-view', args=(kwargs['message_id'],))
        context['detail_mess'] = message
        context['detail_mess_message'] = mark_safe(message.message)
        context['detail_mess_top'] = 'Входящее'
        context['detail_mess_key'] = '1'

        return context


class MessageWriteView(TemplateView):
    template_name = 'auth/user/message/message-write.html'

    @staticmethod
    def post(request):
        if request.is_ajax():
            try:
                to = request.POST.getlist('to[]')
                for id_user in to:
                    user = User.objects.get(id=str(id_user))
                    message = Message.objects.create(user_send=request.user, user_receive=user,
                                                     theme=request.POST['subject'],
                                                     message=request.POST['message'], datetime=datetime.datetime.now())
                    message.save()
                return JsonResponse({'success': True})
            except:
                return JsonResponse({'success': False})

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        users = User.objects.filter(~Q(id=self.request.user.id))
        client = []
        admin = []
        for user in users:
            if hasattr(user, 'client'):
                client.append(user)
            elif hasattr(user, 'administrator'):
                admin.append(user)

        context['client'] = client
        context['admin'] = admin
        return context


class AllMessageView(TemplateView):
    template_name = 'auth/user/message/inbox.html'

    @staticmethod
    def post(request):
        if request.is_ajax():
            if request.POST['key'] == 'makeRead':
                message = Message.objects.get(id=request.POST['id'])
                message.status = 'R'
                message.save()
                return JsonResponse({'success': True})
            elif request.POST['key'] == 'makeImportant':
                message = Message.objects.get(id=request.POST['id'])
                if message.importance == 'U':
                    message.importance = 'I'
                else:
                    message.importance = 'U'
                message.save()
                return JsonResponse({'success': True})
            elif request.POST['key'] == 'makeSpam':
                message = Message.objects.get(id=request.POST['id'])
                message.status = 'S'
                message.save()
                return JsonResponse({'success': True})
            elif request.POST['key'] == 'makeTrash':
                message = Message.objects.get(id=request.POST['id'])
                message.status = 'T'
                message.save()
                return JsonResponse({'success': True})
            elif request.POST['key'] == 'makeDelete':
                message = Message.objects.get(id=request.POST['id'])
                message.delete()
                return JsonResponse({'success': True})

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        messages = Message.objects.filter(Q(user_receive=self.request.user), Q(status='N') |
                                          Q(status='R')).order_by('-id')
        for mess in messages:
            mess.message = mark_safe(mess.message)
            mess.datetime = str(mess.datetime).split(' ')[0]
        context['all_messages'] = messages

        return context


class MessageSendView(TemplateView):
    template_name = 'auth/user/message/outbox.html'

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        messages = Message.objects.filter(Q(user_send=self.request.user), Q(status='N') |
                                          Q(status='R')).order_by('-id')
        for mess in messages:
            mess.message = mark_safe(mess.message)
            mess.datetime = str(mess.datetime).split(' ')[0]
        context['all_messages'] = messages

        return context


class SendDetailView(TemplateView):
    template_name = 'auth/user/message/message-detail.html'

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        # form detail information
        try:
            message = Message.objects.get(Q(user_send=self.request.user),
                                          Q(id=kwargs['message_id']))
        except Message.DoesNotExist:
            raise PermissionDenied

        message.datetime = str(message.datetime).split(' ')[0]
        if hasattr(message.user_receive, 'client'):
            context['detail_mess_avatar'] = message.user_receive.client.avatar
        elif hasattr(message.user_receive, 'administrator'):
            context['detail_mess_avatar'] = message.user_receive.administrator.avatar
        context['detail_mess_url'] = reverse('message-view', args=(kwargs['message_id'],))
        context['detail_mess'] = message
        context['detail_mess_message'] = mark_safe(message.message)
        context['detail_mess_top'] = 'Отправленное'
        context['detail_mess_key'] = '2'

        return context


class MessageSpamView(TemplateView):
    template_name = 'auth/user/message/spam.html'

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        messages = Message.objects.filter(Q(user_receive=self.request.user), Q(status='S')).order_by('-id')
        for mess in messages:
            mess.message = mark_safe(mess.message)
            mess.datetime = str(mess.datetime).split(' ')[0]
        context['all_messages'] = messages

        return context


class MessageTrashView(TemplateView):
    template_name = 'auth/user/message/trash.html'

    def get_context_data(self, **kwargs):
        base = BaseDir()
        context = base.get_data(self)

        messages = Message.objects.filter(Q(user_receive=self.request.user), Q(status='T')).order_by('-id')
        for mess in messages:
            mess.message = mark_safe(mess.message)
            mess.datetime = str(mess.datetime).split(' ')[0]
        context['all_messages'] = messages

        return context


# Rest
# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')





