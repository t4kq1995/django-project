from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse


class LoginView(TemplateView):
    template_name = 'login.html'

    @staticmethod
    def post(request):
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.is_ajax():
                    return JsonResponse({'success': True})
                else:
                    return HttpResponseRedirect('index')
            else:
                if request.is_ajax():
                    return JsonResponse({'success': False})
                else:
                    return HttpResponseRedirect('error/500')
        else:
            if request.is_ajax():
                    return JsonResponse({'success': False})
            else:
                return HttpResponseRedirect('error/500')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context



