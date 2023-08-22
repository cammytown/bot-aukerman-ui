from django.db import models

class Performance(models.Model):
    name = models.TextField()
    description = models.TextField()
    characters = models.ManyToManyField("Character")

class Character(models.Model):
    name = models.TextField()
    description = models.TextField()

class Scene(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
