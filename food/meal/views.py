from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.views.generic.edit import UpdateView
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .utils import *


class FoodHome(DataMixin, ListView):
    model = Food
    template_name = 'meal/index.html'
    context_object_name = 'posts'

    # Динамический контекст для передачи в шаблон
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Food.objects.filter(is_published=True).select_related('cat')


class FoodCategory(DataMixin, ListView):
    model = Food
    template_name = 'meal/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)

        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Food.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


class ShowPost(DataMixin, DetailView):
    model = Food
    template_name = 'meal/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])

        if not context['post'].is_published:
            c_def['cat_selected'] = -1
            c_def['breadcrumbs_extra'] = {
                'name': 'Неопубликованные записи',
                'url': reverse('unpublished_posts')
            }
        else:
            c_def['cat_selected'] = context['post'].cat.pk

        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'meal/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def form_valid(self, form):
        user = self.request.user
        time_limit = timezone.now() - timedelta(days=1)
        recent_posts_count = Food.objects.filter(author=user, time_create__gte=time_limit, is_published=True).count()

        if not user.is_superuser and recent_posts_count >= 3:
            if form.cleaned_data.get('is_published'):
                messages.error(self.request, 'Вы можете добавлять не более 3 опубликованных постов за сутки! '
                                             'Вы можете сохранить запись как неопубликованную.')

                return self.form_invalid(form)
            else:
                messages.success(self.request, 'Пост перемещен в неопубликованные записи!')
                form.instance.author = user

                return super().form_valid(form)

        if not form.cleaned_data.get('is_published'):
            form.instance.author = user
            messages.success(self.request, 'Пост перемещен в неопубликованные записи!')
        else:
            form.instance.author = user
            messages.success(self.request, 'Пост успешно добавлен!')

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)

        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")

        return dict(list(context.items()) + list(c_def.items()))


class EditPostView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Food
    form_class = AddPostForm
    template_name = 'meal/editpost.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f"Редактирование поста - {self.object.title}")
        context['extra_links'] = [{'title': 'Вернуться к посту', 'url': self.object.get_absolute_url()}]

        return dict(list(context.items()) + list(c_def.items()))

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if not self.request.user.is_superuser and obj.author != self.request.user:
            messages.error(self.request, 'Вы не можете редактировать этот пост!')

            return reverse_lazy('home')

        return obj

    def form_valid(self, form):
        user = self.request.user
        time_limit = timezone.now() - timedelta(days=1)
        recent_posts_count = Food.objects.filter(author=user, time_create__gte=time_limit, is_published=True).count()

        post = self.object
        is_published = form.cleaned_data.get('is_published')

        if is_published:
            if not user.is_superuser and recent_posts_count >= 3:
                messages.error(self.request, 'Вы не можете опубликовать более 3 постов за сутки!')

                return self.form_invalid(form)

            messages.success(self.request, 'Пост успешно опубликован!')
            post.is_published = True
        else:
            messages.success(self.request, 'Изменения сохранены, пост остается неопубликованным.')
            post.is_published = False

        post.save()
        return redirect(post.get_absolute_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class UnpublishedPostsView(LoginRequiredMixin, DataMixin, ListView):
    model = Food
    template_name = 'meal/unpublished_posts.html'
    context_object_name = 'posts'
    login_url = reverse_lazy('home')

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Food.objects.filter(is_published=False).select_related('cat')

        return Food.objects.filter(is_published=False, author=user).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Неопубликованные записи", cat_selected=-1)

        return dict(list(context.items()) + list(c_def.items()))


# @cache_page(60 * 60)
def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu = [item for item in menu if item['url_name'] != 'add_page']

    return render(request, 'meal/about.html', {'menu': user_menu, 'title': 'О сайте'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'meal/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)

        return redirect('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'meal/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")

        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'meal/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")

        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)

    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
