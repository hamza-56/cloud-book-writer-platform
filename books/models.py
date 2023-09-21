from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Book(TimeStampedModel):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name="collaborators")

    def __str__(self):
        return self.title


class Section(TimeStampedModel):
    title = models.CharField(max_length=50)
    text = models.TextField()
    order = models.PositiveIntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sections")
    parent_section = models.ForeignKey(
        "Section", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title}"
