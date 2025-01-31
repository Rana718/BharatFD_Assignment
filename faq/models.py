from django.db import models
from ckeditor.fields import RichTextField


class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question
