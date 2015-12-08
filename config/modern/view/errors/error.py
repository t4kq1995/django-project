__author__ = 't4kq'
from django.views.generic.base import TemplateView


class Error500(TemplateView):
    template_name = 'errors/500.html'

    def get_context_data(self, **kwargs):
        context = super(Error500, self).get_context_data(**kwargs)
        return context


class Error404(TemplateView):
    template_name = 'errors/404.html'

    def get_context_data(self, **kwargs):
        context = super(Error404, self).get_context_data(**kwargs)
        return context
