from django.db import models
from random import shuffle

class Deck(models.Model):
    name = models.CharField(max_length=100)

    def calculate_progress(self):
        """
        Calcula el progreso del mazo basado en el estado de las flashcards.
        """
        total_cards = self.flashcard_set.count()
        if total_cards == 0:
            return 0
        learned_cards = self.flashcard_set.filter(box_number=5).count()
        return (learned_cards / total_cards) * 100

    def create_deck(self, name):
        """
        Crea un nuevo mazo asociado a un usuario.
        """
        new_deck = Deck(name=name)
        new_deck.save()
        return new_deck

    def delete_deck(self):
        """
        Elimina este mazo y todas las flashcards asociadas.
        """
        self.flashcard_set.all().delete()
        self.delete()

    def edit_deck(self, new_name):
        """
        Edita el nombre del mazo.
        """
        self.name = new_name
        self.save()

    def study_flashcards(self, limit=10):
        """
        Devuelve un conjunto de flashcards para estudiar, comenzando desde la caja más baja.
        """
        flashcards = self.flashcard_set.all().order_by('box_number')[:limit]
        flashcards = list(flashcards)
        shuffle(flashcards)
        return flashcards

class FlashCard(models.Model):
    question = models.TextField()
    answer = models.TextField()
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    box_number = models.IntegerField(default=1)

    def mark_learned(self):
        """
        Marca la flashcard como aprendida y la mueve a la siguiente caja si es posible.
        """
        if self.box_number < 5:
            self.box_number += 1
        self.save()

    def mark_not_learned(self):
        """
        Marca la flashcard como no aprendida y la mueve a la caja anterior si es posible.
        """
        if self.box_number > 1:
            self.box_number -= 1
        self.save()

    def reset_to_first_box(self):
        """
        Reinicia la flashcard a la primera caja.
        """
        self.box_number = 1
        self.save()
