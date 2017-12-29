from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import *
from .forms import *
from django.utils import timezone
from datetime import timedelta


class IndexView(TemplateView):
    template_name = 'pages/file_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['files'] = UploadFiles.objects.filter(file_time__gte=timezone.now()-timedelta(days=8))
        return context


class UploadView(CreateView):
    form_class = FormUploadFiles
    template_name = 'pages/file_upload.html'
    success_url = '/'
