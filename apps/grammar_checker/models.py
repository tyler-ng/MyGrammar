from django.db import models
from django.utils import timezone

class GrammarCheck(models.Model):
    original_text = models.TextField()
    refine_text = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Grammar Check {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
