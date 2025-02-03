import uuid

from django.db import models


class OnlyActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)

    objects = models.Manager()
    active_objects = OnlyActiveManager()

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def undelete(self, *args, **kwargs):
        self.is_active = True
        self.save()

    def permanent_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ("-updated_at",)
