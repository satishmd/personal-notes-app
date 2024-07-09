from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

# modify user model to include email
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

class Notes(models.Model):
    title = models.CharField(max_length=250, null=False)
    body = models.TextField(null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = "notes"

