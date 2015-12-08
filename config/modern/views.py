from django.http import HttpResponseRedirect


def check_authenticated(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('index')
    else:
        return HttpResponseRedirect('login')


