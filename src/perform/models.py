from django.db import models

class Performance(models.Model):
    title = models.TextField(null=True, blank=True)

    #@REVISIT this is a scene description; but not using Scene yet
    # description = models.TextField()

    scenes = models.ManyToManyField("Scene")
    characters = models.ManyToManyField("Character")

    #@TODO probably move into Scene
    script = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Character(models.Model):
    name = models.TextField()
    description = models.TextField()

class Scene(models.Model):
    # name = models.TextField()
    description = models.TextField()
