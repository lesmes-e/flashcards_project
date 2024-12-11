from django.db import models
from django.contrib.auth.models import User

class Mazo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacionamos un mazo con un usuario
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

    def get_progreso(self):
        """Calcula el progreso de un mazo, por ejemplo, cuántas tarjetas están completadas."""
        flashcards = Flashcard.objects.filter(mazo=self)
        completadas = flashcards.filter(completada=True)
        if flashcards.count() > 0:
            return round((completadas.count() / flashcards.count()) * 100, 2)
        return 0

class Flashcard(models.Model):
    mazo = models.ForeignKey(Mazo, on_delete=models.CASCADE, related_name="flashcards")
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    completada = models.BooleanField(default=False)  # Para marcar si la tarjeta ha sido revisada o completada

    def __str__(self):
        return f"Pregunta: {self.pregunta}"

    def toggle_completada(self):
        """Método para cambiar el estado de completada."""
        self.completada = not self.completada
        self.save()

    def get_estado(self):
        """Devuelve el estado de la flashcard."""
        return "Completada" if self.completada else "Pendiente"