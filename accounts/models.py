from django.db import models
from django.contrib.auth.models import AbstractUser
import os
# Create your models here.

class User(AbstractUser):
    Role_Choice = {
        ("mess_provider", "Mess_Provider"),
        ("customer", "Customer"),
        ("admin", "Admin")
    }
    role = models.CharField(max_length=10, choices=Role_Choice)
    
def customer_profile_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'profile_photo.{ext}'
    return os.path.join('students', f'user_{instance.user.id}', new_filename)

def provider_profile_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f'mess_photo.{ext}'
    return os.path.join('providers', f'user_{instance.user.id}', new_filename)

class MessProviderProfile(models):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='MessProviderProfile')
    image = models.ImageField(upload_to= provider_profile_photo_path, height_field=None, width_field=None, max_length=None)
    