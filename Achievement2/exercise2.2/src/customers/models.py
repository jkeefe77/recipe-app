from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=120)
    notes = models.TextField()

    def __str__(Self):
        return Self.name
