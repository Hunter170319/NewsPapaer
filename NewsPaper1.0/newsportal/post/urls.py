from django.urls import path,include
from .views import PostDetail, NewsList, ArticleList, NotificationList, PostCreate, PostHome, PostEdit, PostDelete
from .forms import PostForm
from django.contrib import admin


urlpatterns = [
    path('', PostHome.as_view(), name='portal_home'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('news/', NewsList.as_view(), name='news_list'),
    path('article/', ArticleList.as_view(), name='article_list'),
    path('notification/', NotificationList.as_view(), name='notification_list'),
]