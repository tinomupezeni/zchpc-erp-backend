from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    employeeid = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.email

class Employee(models.Model):
    firstname = models.CharField(max_length=100)
    email = models.EmailField()
    surname = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    employeeid = models.CharField(max_length=100, unique=True)
    salary = models.IntegerField()
    contractFrom = models.DateField()  # Use DateField for dates
    contractTo = models.DateField()

    def __str__(self):
        return f"{self.firstname} {self.surname}"