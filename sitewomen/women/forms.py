from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, Women



class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    # husband = forms.ModelChoiceField(queryset=Husband.objects.all(), empty_label="Не замужем", required=False,
    #                                  label="Муж")

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'row': 5})
        }
        labels = {"slug": 'URL'}


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')
