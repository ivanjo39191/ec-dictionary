
import os
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.urls import reverse
from django_tenants_q.utils import QUtilities

from django_tenants.management.commands.clone_tenant import Command


from random import choice

from ecdict.crawler import crawler
from ecdict.forms import ECDictForm
from ecdict.models import Dictionary, Vocabulary, Expatiation

@method_decorator(never_cache, name='dispatch')
class ECDictFormView(LoginRequiredMixin, FormView):
    login_url = '/admin/login/'
    template_name = 'ecdict/ecdict_form.html'
    form_class = ECDictForm

    def get_context_data(self, **kwargs):
        context = super(ECDictFormView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        dictionary = form.cleaned_data['dictionary']
        dictionary_obj = Dictionary.objects.filter(name=dictionary).first()
        vocabulary_list = form.cleaned_data['vocabulary'].split('\n')
        success_list = []
        failure_list = []
        for vocabulary in vocabulary_list:
            ec_dict = crawler(vocabulary)
            if ec_dict:
                if not (vocabulary_queryset := Vocabulary.objects.filter(name_en=ec_dict.get('name_en'))):
                    vocabulary_obj = Vocabulary.objects.create(name_en=ec_dict.get('name_en'))
                    vocabulary_obj.kk = ec_dict.get('kk')
                    vocabulary_obj.save()
                    for expatiation in ec_dict.get('part_of_speech'):
                        Expatiation.objects.create(vocabulary=vocabulary_obj, part_of_speech=expatiation[0], name_zh=expatiation[1])
                else:
                    vocabulary_obj = vocabulary_queryset.first()
                dictionary_obj.vocabulary.add(vocabulary_obj)
                success_list.append(vocabulary)
            else:
                failure_list.append(vocabulary)
        context = {}
        context['success_list'] = success_list if success_list else '無'
        context['failure_list'] = failure_list if failure_list else '無'
        context['success_header'] = ['轉入成功單字']
        context['failure_header'] = ['轉入失敗單字']
        self.request.current_app = 'admin'
        context.update(admin.site.each_context(self.request))
        return render(self.request, 'ecdict/ecdict_result.html', context)
        # return HttpResponseRedirect(reverse('admin:ecdict_dictionary_changelist'))

    def get_success_url(self):
        return reverse('admin:ecdict_dictionary_changelist')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            context = self.get_context_data(**kwargs)
            request.current_app = 'admin'
            context.update(admin.site.each_context(request))
            return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        # 限制特定使用者才可進入該頁面
        if not request.user.username.startswith('admin') and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))
        context = self.get_context_data(**kwargs)
        request.current_app = 'admin'
        context.update(admin.site.each_context(request))
        return self.render_to_response(context)