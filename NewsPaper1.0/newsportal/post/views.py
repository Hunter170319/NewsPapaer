from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect

from .models import Post, Subscription, Category
from .filters import PostFilter
from .forms import PostForm, EditForm

@login_required
@csrf_protect
def subscriptions(request, categories=None):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, post=post)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                post=post,
            ).delete()

    posts_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                post=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'posts': posts_with_subscriptions},
    )


class PostDetail(DetailView):
    # Модель по которой мы хотим получать информацию по отдельной статье
    model = Post
    # Используем другой шаблон — post_detail.html
    template_name = "post/post_detail.html"
    # Название объекта, в котором будет выбранная пользователем статья
    context_object_name = "postdetail"


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/home.html'
    context_object_name = 'postlist'
    paginate_by = 10  # количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'post/news_list.html'
    context_object_name = 'newslist'
    paginate_by = 10  # количество записей на странице

    # Переопределяем функцию получения списка товаров
    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict, который мы рассматривали
    #     # в этом юните ранее.
    #     # Сохраняем нашу фильтрацию в объекте класса,
    #     # чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список товаров
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Добавляем в контекст объект фильтрации.
    #     context['filterset'] = self.filterset
    #     return context


class ArticleList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'post/article_list.html'
    context_object_name = 'articlelist'
    paginate_by = 10  # количество записей на странице

    # Переопределяем функцию получения списка товаров
    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict, который мы рассматривали
    #     # в этом юните ранее.
    #     # Сохраняем нашу фильтрацию в объекте класса,
    #     # чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список товаров
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Добавляем в контекст объект фильтрации.
    #     context['filterset'] = self.filterset
    #     return context


class NotificationList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'post/notification_list.html'
    context_object_name = 'notificationlist'
    paginate_by = 10  # количество записей на странице

    # Переопределяем функцию получения списка товаров
    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict, который мы рассматривали
    #     # в этом юните ранее.
    #     # Сохраняем нашу фильтрацию в объекте класса,
    #     # чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список товаров
    #     return self.filterset.qs
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Добавляем в контекст объект фильтрации.
    #     context['filterset'] = self.filterset
    #     return context


class PostCreate(PermissionRequiredMixin,CreateView):
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post/post_create.html'


class PostSearch(ListView):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filterset_class = PostFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostHome(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/home.html'
    context_object_name = 'postlist'
    paginate_by = 10  # количество записей на странице


class PostEdit(PermissionRequiredMixin,UpdateView):
    form_class = EditForm
    model = Post
    template_name = 'post/post_edit.html'

    def form_valid(self, form):
        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin,DeleteView):
    model = Post
    template_name = 'post/post_delete.html'
    context_object_name = 'postdelete'

    def form_valid(self, form):
        self.object.delete()
        return redirect('portal_home')
