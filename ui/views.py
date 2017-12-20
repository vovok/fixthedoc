from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import *


class IndexView(TemplateView):
    template_name = 'pages/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        # TODO: сделать выборку за последнюю неделю
        context['files'] = UploadFiles.objects.all()
        return context


class UploadView(CreateView):
    form_class = FormUploadFiles
    template_name = 'pages/file_upload.html'
    success_url = '/'
