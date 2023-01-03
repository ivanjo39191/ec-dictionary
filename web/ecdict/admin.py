from django.contrib import admin
from ecdict.models import Dictionary, Vocabulary, Expatiation
admin.autodiscover()
admin.site.enable_nav_sidebar = False

class VocabularyInline(admin.TabularInline):
    search_fields = ['vocabulary']
    model = Dictionary.vocabulary.through
    autocomplete_fields = (
        'vocabulary',
    )
    fields = ('vocabulary', 'kk', 'expatiation')
    readonly_fields = ('kk', 'expatiation',)
    

class DictionaryInline(admin.TabularInline):
    search_fields = ['dictionary']
    model = Dictionary.vocabulary.through
    autocomplete_fields = (
        'dictionary',
    )


class ExpatiationInline(admin.TabularInline):
    model = Expatiation
    search_fields = ['name_zh']
    fields = ('name_zh', 'part_of_speech', 'created', 'modified',)
    # fields = ('name_zh', 'part_of_speech', 'example_sentences', 'created', 'modified',)
    list_display = ('name_zh',)
    readonly_fields = ('created', 'modified')


class DictionaryAdmin(admin.ModelAdmin):
    change_list_template = "ecdict/change_list.html"
    search_fields = ['name']
    fields = ('name', 'created', 'modified')
    list_display = ('name',)
    list_filter = ('name',)
    readonly_fields = ('created', 'modified')
    inlines = [VocabularyInline, ]


class VocabularyAdmin(admin.ModelAdmin):
    search_fields = ['name_en', ]
    fields = ('name_en', 'kk', 'created', 'modified',)
    list_display = ('name_en', 'kk', 'get_expatiation')
    readonly_fields = ('created', 'modified')
    inlines = [ExpatiationInline, DictionaryInline, ]

    def get_expatiation(self, obj):
        expatiation_objs = obj.expatiation_set.all()
        text_list = []
        for expatiation_obj in expatiation_objs:
            text_list.append(expatiation_obj.part_of_speech + ' ' + expatiation_obj.name_zh)
        text = "\n".join([text for text in text_list])
        return text
    get_expatiation.short_description = '釋義'

admin.site.register(Dictionary, DictionaryAdmin)         # 註冊 Dictionary 模型
admin.site.register(Vocabulary, VocabularyAdmin)    # 註冊 Vocabulary 模型


