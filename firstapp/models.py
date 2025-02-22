# from django.db import models

# Create your models here.
# your_app/models.py
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class ChatMessage(models.Model):
    """
    Model to store user messages and chatbot responses.
    """
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('chatbot', 'ChatBot')])
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message} ({self.timestamp})"

    class Meta:
        ordering = ['timestamp'] # Ensure messages are displayed in chronological order