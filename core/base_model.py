from django.db import models


class RootModelManager(models.Manager):
    """
    base manager for base model
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class RootModel(models.Model):
    """
    base model
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, serialize=False)

    objects = RootModelManager()

    def delete(self, *args, **kwargs) -> tuple:
        self.is_deleted = True
        self.save()
        return tuple()

    class Meta:
        abstract = True