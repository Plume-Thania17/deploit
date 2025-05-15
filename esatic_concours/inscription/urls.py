from django.urls import path
from . import views

urlpatterns = [  # <-- Utilisez des crochets [] au lieu d'accolades {}
    path('', views.accueil, name='accueil'), 
    path('inscription.html/', views.inscription, name='inscription'),
    path('felicitation/', views.felicitation, name='felicitation'),
]