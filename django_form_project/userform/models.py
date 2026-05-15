from django.db import models

class UserFormData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name