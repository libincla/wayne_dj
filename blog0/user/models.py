from django.db import models

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=256)
    password = models.CharField(max_length=255)

    def __repr__(self):
        return  '{} {}' % (self.name, self.email)

    __str__ = __repr__