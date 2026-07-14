from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=18)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name