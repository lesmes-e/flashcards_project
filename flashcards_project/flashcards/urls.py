from django.urls import path
from . import views

urlpatterns = [
    # Ruta para el dashboard
    path('', views.list_decks, name=' '),

    # Rutas para los mazos (Decks)
    path('decks/', views.list_decks, name='list_decks'),
    path('decks/create/', views.create_deck, name='create_deck'),
    path('decks/<int:deck_id>/edit/', views.edit_deck, name='edit_deck'),
    path('decks/<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),

    # Rutas para las flashcards en un mazo específico
    path('decks/<int:deck_id>/flashcards/', views.list_flashcards, name='list_flashcards'),
    path('decks/<int:deck_id>/flashcards/create/', views.create_flashcard, name='create_flashcard'),
    path('flashcards/<int:flashcard_id>/edit/', views.edit_flashcard, name='edit_flashcard'),
    path('flashcards/<int:flashcard_id>/delete/', views.delete_flashcard, name='delete_flashcard'),
    path('decks/<int:deck_id>/study/', views.study_flashcards, name='study_flashcards'),


    # Rutas para marcar flashcards como aprendidas o no aprendidas
    path('flashcards/<int:flashcard_id>/mark-learned/', views.mark_flashcard_learned, name='mark_flashcard_learned'),
    path('flashcards/<int:flashcard_id>/mark-not-learned/', views.mark_flashcard_not_learned, name='mark_flashcard_not_learned'),
]
