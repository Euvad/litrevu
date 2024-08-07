from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='ticket_images/', blank=True, null=True)  # Nouveau champ
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
