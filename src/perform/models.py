from django.db import models
from datetime import datetime

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super(SoftDeleteManager, self).get_queryset().filter(is_deleted=False)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True) #@ do we care?

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def soft_delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        self.save()

    class Meta:
        abstract = True

class Performance(SoftDeleteModel):
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

    #@REVISIT naming/architecture
    performer = models.CharField(max_length=255)

class Scene(models.Model):
    # name = models.TextField()
    description = models.TextField()
