from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class CustomManager(models.Manager):
    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(isDeleted=False)


class CustomModel(models.Model):
    createdAt = models.DateTimeField(default=timezone.now)
    modifiedAt = models.DateTimeField(default=timezone.now)
    isDeleted = models.BooleanField(default=False)
    objects = CustomManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id or not self.createdAt:
            self.createdAt = timezone.now()
        self.modifiedAt = timezone.now()
        super(CustomModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.isDeleted = True
        super(CustomModel, self).save(*args, **kwargs)

    def hard_delete(self, *args, **kwargs):
        super(CustomModel, self).delete(*args, **kwargs)


class DynamicValidationMixin:
    REQUIRED_FIELDS = []

    def clean(self):
        for field in self.REQUIRED_FIELDS:
            field_value = getattr(self, field, None)
            if not field_value:
                raise ValidationError(f"{field} is required.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)  # Call the model's default save method