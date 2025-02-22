# from django.db import models

# Create your models here.
# your_app/models.py
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=False)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email