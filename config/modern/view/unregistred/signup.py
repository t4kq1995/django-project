# -*- coding: utf-8 -*-
__author__ = 't4kq'
import datetime
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from modern.models import Notification, Client, Message, Administrator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from random import randint


class SignUp(TemplateView):
    template_name = 'registration/register.html'

    @staticmethod
    def send_message(model):
        # get all admins
        admins = Administrator.objects.all()

        id_admin = randint(0, len(admins)-1)

        # send message
        message = Message.objects.create(user_send=admins[id_admin].user, user_receive=model,
                                         theme='Добро пожаловать на наш проект',
                                         message='Привет', datetime=datetime.datetime.now())
        message.save()

    @staticmethod
    def make_notification(model):
        notification = Notification.objects.create(user=model, message='Добро пожаловать',
                                                   type='I', status='N', datetime=datetime.datetime.now())
        notification.save()

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        login = request.POST['login']
        email = request.POST['email']
        password = request.POST['password']

        # Check email
        user = User.objects.filter(Q(email=email) | Q(username=login))

        if not user:
            # Save new user
            user = User.objects.create(first_name=name, last_name=surname, email=email,
                                       username=login, password=make_password(password))
            user.save()

            # Save profile
            Client.objects.create(user=user, online=datetime.datetime.now()).save()

            # Make notification
            self.make_notification(user)

            # Send message
            self.send_message(user)
            print 'qq'
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        return context


class ForgotPassword(TemplateView):
    template_name = 'registration/forgot.html'

    @staticmethod
    def post(request):
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            user = None

        if user is not None:
            # send_mail('Восстановление пароля', 'Ваш пароль : ' + user.password, 'admin@modern.zp.ua',
            #           [email], fail_silently=False)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    def get_context_data(self, **kwargs):
        context = super(ForgotPassword, self).get_context_data(**kwargs)
        return context



