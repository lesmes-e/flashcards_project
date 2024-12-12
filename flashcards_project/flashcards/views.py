from django.shortcuts import render, get_object_or_404, redirect
from .models import Deck, FlashCard

def list_decks(request):
    """
    Muestra todos los mazos disponibles para el usuario.
    """
    decks = Deck.objects.all()
    ranking = FlashCard.objects.order_by('-repeat_count')[:5]  # Agregar el ranking de flashcards
    return render(request, 'flashcards/dashboard.html', {'decks': decks, 'ranking': ranking})

def create_deck(request):
    """
    Crea un nuevo mazo.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        deck = Deck(name=name)
        deck.save()
        return redirect('list_decks')
    return render(request, 'flashcards/create_deck.html')

def edit_deck(request, deck_id):
    """
    Edita un mazo existente.
    """
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        new_name = request.POST.get('name')
        deck.edit_deck(new_name)
        return redirect('list_decks')
    return render(request, 'flashcards/edit_deck.html', {'deck': deck})

def delete_deck(request, deck_id):
    """
    Elimina un mazo existente.
    """
    deck = get_object_or_404(Deck, id=deck_id)
    deck.delete_deck()
    return redirect('list_decks')

def list_flashcards(request, deck_id):
    """
    Muestra todas las flashcards de un mazo específico.
    """
    deck = get_object_or_404(Deck, id=deck_id)
    flashcards = deck.flashcard_set.all()
    return render(request, 'flashcards/list_flashcards.html', {'deck': deck, 'flashcards': flashcards})

def create_flashcard(request, deck_id):
    """
    Crea una nueva flashcard en un mazo específico.
    """
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        flashcard = FlashCard(deck=deck, question=question, answer=answer)
        flashcard.save()
        return redirect('list_flashcards', deck_id=deck.id)
    return render(request, 'flashcards/create_flashcard.html', {'deck': deck})

def edit_flashcard(request, flashcard_id):
    """
    Edita una flashcard existente.
    """
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    if request.method == 'POST':
        flashcard.question = request.POST.get('question')
        flashcard.answer = request.POST.get('answer')
        flashcard.save()
        return redirect('list_flashcards', deck_id=flashcard.deck.id)
    return render(request, 'flashcards/edit_flashcard.html', {'flashcard': flashcard})

def delete_flashcard(request, flashcard_id):
    """
    Elimina una flashcard existente.
    """
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    deck_id = flashcard.deck.id
    flashcard.delete()
    return redirect('list_flashcards', deck_id=deck_id)

def mark_flashcard_learned(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    flashcard.mark_learned()
    return redirect('study_flashcards', deck_id=flashcard.deck.id)

def mark_flashcard_not_learned(request, flashcard_id):
    flashcard = get_object_or_404(FlashCard, id=flashcard_id)
    flashcard.mark_not_learned()
    return redirect('study_flashcards', deck_id=flashcard.deck.id)

def study_flashcards(request, deck_id):
    """
    Muestra un conjunto de flashcards para estudiar.
    """
    deck = get_object_or_404(Deck, id=deck_id)
    flashcards = deck.study_flashcards(limit=10)
    return render(request, 'flashcards/study_flashcards.html', {'deck': deck, 'flashcards': flashcards})