from django.db import models

class Performance(models.Model):
    title = models.TextField(null=True, blank=True)
    # description = models.TextField()
    characters = models.ManyToManyField("Character")
    script = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Character(models.Model):
    name = models.TextField()
    description = models.TextField()

class Scene(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    # name = models.TextField()
    description = models.TextField()
