from keyword import kwlist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.transaction import commit
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify, title
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, CreateView, DeleteView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    paginate_by = 5

    def get_queryset(self):
        return Women.published.all().select_related('cat')




def about(request):

    return render(request, 'women/about.html',
                  {'title': 'О сайте'})


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title, cat_selected=1)

    def get_object(self, queryset=None):
        post = get_object_or_404(Women, slug=self.kwargs[self.slug_url_kwarg])

        # Только автор или staff могут видеть черновик
        if not post.is_published and self.request.user != post.author and not self.request.user.is_staff:
            raise Http404("Черновик недоступен")
        return post


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


# class UpdatePage(DataMixin, UpdateView):
#     model = Women
#     fields = ['title', 'content', 'photo', 'is_published', 'cat']
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')
#     title_page = 'Редактирование статьи'


class UpdatePage(DataMixin, UpdateView):
    model = Women
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Редактирование: {self.object.title}')

    def form_valid(self, form):
        form.instance.author = self.request.user  # Сохраняем автора
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект до обработки запроса
        self.object = self.get_object()

        # Проверяем права
        if self.object.author != request.user and not request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)



class DeletePost(LoginRequiredMixin, DeleteView):
    model = Women
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('home')
    template_name = 'women/confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        # Проверка прав доступа
        post = self.get_object()
        if post.author != request.user and not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Пост успешно удален!')
        return super().delete(request, *args, **kwargs)



class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        posts = Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name,
                                      cat_selected=cat.pk)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")



class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).prefetch_related("tags")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=f"Тег: {tag.tag}")

