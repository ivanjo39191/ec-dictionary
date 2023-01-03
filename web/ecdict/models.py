from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Dictionary(models.Model):
    '''
    英漢單字本
    '''
    dict_id = models.CharField(_('Order Id'), max_length=20)
    name = models.CharField(_('Name'), max_length=50)
    vocabulary = models.ＭanyToManyField(
        'ecdict.Vocabulary', blank=True, 
        verbose_name=_('Vocabulary'), related_name='dictionary_set',
        through='ecdict.RelationalDictionary'
    )
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.dict_id:
            self.dict_id = f'DICT{self.id:08}'
            super().save(*args, **kwargs)
    class Meta:
        verbose_name = '英漢單字本'
        verbose_name_plural = '英漢單字本'

    def __str__(self):
        return f'{self.name}'

class Vocabulary(models.Model):
    '''
    英漢單字
    '''
    name_en = models.CharField(_('English Name'), max_length=255)
    name_zh = models.CharField(_('Chinese Name'), max_length=255)
    kk = models.CharField(_('讀音'), blank=True, null=True, max_length=255)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True)

    class Meta:
        verbose_name = '英漢單字'
        verbose_name_plural = '英漢單字'
        ordering = ['name_en']

    def __str__(self):
        return f'{self.name_en}'

class RelationalDictionary(models.Model):
    dictionary = models.ForeignKey('ecdict.Dictionary', on_delete=models.CASCADE, verbose_name='單字本')
    vocabulary = models.ForeignKey('ecdict.Vocabulary', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = '英漢單字列表'
        verbose_name_plural = '英漢單字列表'
        ordering = ['vocabulary__name_en']
        
    def __str__(self):
        return ""

    @property
    def kk(self):
        if not self.vocabulary.kk:
            return ''
        return self.vocabulary.kk
    kk.fget.short_description = 'KK'

    @property
    def expatiation(self):
        expatiation_objs = self.vocabulary.expatiation_set.all()
        text_list = []
        for expatiation_obj in expatiation_objs:
            text_list.append(expatiation_obj.part_of_speech + ' ' + expatiation_obj.name_zh)
        text = "\n".join([text for text in text_list])
        return text
    expatiation.fget.short_description = '釋義'



    

class Expatiation(models.Model):
    '''
    釋義
    '''
    vocabulary = models.ForeignKey('ecdict.Vocabulary', on_delete=models.CASCADE, related_name='expatiation_set')
    part_of_speech = models.CharField(_('詞性'), max_length=255)
    name_zh = models.CharField(_('釋義'), max_length=255)
    example_sentences = models.TextField('例句', max_length=1000, null=True, blank=True)
    created = models.DateTimeField(_('Created Date'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True)

    class Meta:
        verbose_name = '釋義'
        verbose_name_plural = '釋義'

    def __str__(self):
        return f'{self.name_zh}'