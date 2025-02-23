from django.db import models
from django.utils import timezone

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
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='chat_messages')

    def __str__(self):
        return f"{self.sender}: {self.message} ({self.timestamp})"

    class Meta:
        ordering = ['timestamp'] # Ensure messages are displayed in chronological order

def get_chat_history_for_subscriber(email):
    """
    Retrieves the chat history as a list of dictionaries for a given subscriber email.

    Args:
        email (str): The email address of the subscriber.

    Returns:
        list: A list of dictionaries, where each dictionary represents a chat message.
              Each dictionary contains 'sender', 'message', and 'timestamp'.
              Returns an empty list if the subscriber or chat history is not found.
    """
    try:
        subscriber = Subscriber.objects.get(email=email)
        chat_messages = subscriber.chat_messages.all()

        chat_history = []
        for message in chat_messages:
            chat_history.append({
                'sender': message.sender,
                'message': message.message,
                'timestamp': message.timestamp.isoformat() # Convert datetime to ISO format for JSON serialization
            })

        return chat_history

    except Subscriber.DoesNotExist:
        return [] # Return empty list if subscriber does not exist

def create_chat_message(email, sender, message):
    """
    Creates a new chat message associated with a subscriber.

    Args:
        email (str): The email address of the subscriber.
        sender (str): The sender of the message ('user' or 'chatbot').
        message (str): The content of the message.
    """
    try:
        subscriber = Subscriber.objects.get(email=email)
        ChatMessage.objects.create(subscriber=subscriber, sender=sender, message=message)
    except Subscriber.DoesNotExist:
        # Handle the case where the subscriber doesn't exist (e.g., create a new subscriber or log an error)
        print(f"Subscriber with email {email} does not exist.")
        #example of creating a new user if they do not exist.
        #subscriber=Subscriber.objects.create(email=email)
        #ChatMessage.objects.create(subscriber=subscriber, sender=sender, message=message)