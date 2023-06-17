from django.urls import path
from . import views



urlpatterns = [
   path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('provider', views.provider, name='provider'),
    path('edit_provider/<provide_id>', views.edit_provider, name='edit_provider'),
    path('new_provider', views.new_provider, name='new_provider'),
    path('delete_provider/<provide_id>', views.delete_provider, name='delete_provider'),
    path('article', views.article, name='article'),
    path('edit_article/<article_id>', views.edit_article, name='edit_article'),
    path('new_article', views.new_article, name='new_article'),
    path('delete_article/<article_id>', views.delete_article, name='delete_article'),
    path('client', views.client, name='client'),
    path('edit_client/<client_id>', views.edit_client, name='edit_client'),
    path('new_client', views.new_client, name='new_client'),
    path('delete_client/<client_id>', views.delete_client, name='delete_client'),
    
]


