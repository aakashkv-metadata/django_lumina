from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add custom fields here if needed
    pass
    
    def __str__(self):
        return self.username
