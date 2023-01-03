
from django import forms
from django.db import models
from ecdict.models import Dictionary, Vocabulary, Expatiation
from ecdict.crawler import crawler

class ECDictForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(ECDictForm, self).__init__(*args, **kwargs)
        self.fields['dictionary'].label = "單字本名稱"
        self.fields['vocabulary'].label = "單字表"
        self.fields['vocabulary'].widget = forms.Textarea(attrs={'rows': 10, 'cols': 90})

    
    dictionary = forms.CharField(required=True)
    vocabulary = forms.CharField(required=True)

    def clean_dictionary(self):
        data = self.cleaned_data['dictionary']

        return data

    def clean(self):
        dictionary = self.cleaned_data['dictionary']
        if not (dictionary_queryset := Dictionary.objects.filter(name=dictionary)):
            raise forms.ValidationError(f'單字本 "{dictionary}" 不存在。')
        # else:
        #     dictionary_obj = dictionary_queryset.first()
        # vocabulary_list = self.cleaned_data['vocabulary'].split('\n')
        # for vocabulary in vocabulary_list:
        #     ec_dict = crawler(vocabulary)
        #     if ec_dict:
        #         if not (vocabulary_queryset := Vocabulary.objects.filter(name_en=ec_dict.get('name_en'))):
        #             vocabulary_obj = Vocabulary.objects.create(name_en=ec_dict.get('name_en'))
        #             vocabulary_obj.kk = ec_dict.get('kk')
        #             vocabulary_obj.save()
        #             for expatiation in ec_dict.get('part_of_speech'):
        #                 Expatiation.objects.create(vocabulary=vocabulary_obj, part_of_speech=expatiation[0], name_zh=expatiation[1])
        #         else:
        #             vocabulary_obj = vocabulary_queryset.first()
        #         dictionary_obj.vocabulary.add(vocabulary_obj)
