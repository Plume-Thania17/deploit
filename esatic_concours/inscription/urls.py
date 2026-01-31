from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('felicitation/', views.felicitation, name='felicitation'),
    path('contact/', views.contact, name='contact'),
    path('telecharger-recu/<int:inscription_id>/', views.telecharger_recu, name='telecharger_recu'),
    path('telecharger-convocation/<int:inscription_id>/', views.telecharger_convocation, name='telecharger_convocation'),
]