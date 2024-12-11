from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mazo/<int:mazo_id>/', views.flashcard_list, name='flashcard_list'),
    path('mazo/<int:mazo_id>/add_flashcard/', views.add_flashcard, name='add_flashcard'),
    path('flashcard/<int:flashcard_id>/toggle/', views.toggle_flashcard, name='toggle_flashcard'),
    path('create_mazo/', views.create_mazo, name='create_mazo'),
]

