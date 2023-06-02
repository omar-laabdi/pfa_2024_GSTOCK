from django.urls import path
from . import views

urlpatterns = [
    path('caisse', views.caisse, name='caisse'),
    path('paiement', views.paiement, name='paiement'),
    path('retour', views.retour, name='retour'),
    path('delete/<int:article_id>', views.delete_article, name='delete_article'),
    path('delete/all/<str:barcode>/', views.delete_all_articles, name='delete_all_articles'),

]

