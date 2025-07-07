from django.contrib import admin
from .models import Women, Category, Husband
from django.contrib import messages
from unfold.admin import ModelAdmin

# Register your models here.


admin.site.site_header = 'Админка'
admin.site.index_title = '-------'



class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(husband__isnull=False)
        else:
            return queryset


@admin.register(Women)
class WomenAdmin(ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags']
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ['tags']
    list_display = ('id', 'title', 'time_create', 'is_published', 'bref_info')
    list_display_links = ('id', 'title')
    ordering = ('time_create', 'title')
    list_editable = ('is_published', )
    list_per_page = 5
    actions = ['set_published', 'reset_published']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']


    @admin.display(description='Краткое описание')
    def bref_info(self, women: Women):
        return f'Описание {len(women.content)} символов'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        cont = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Изменено {cont} записей')

    @admin.action(description='Снять выбранные записи')
    def reset_published(self, request, queryset):
        cont = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{cont} записей снято с публикации', messages.WARNING)



@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', )




