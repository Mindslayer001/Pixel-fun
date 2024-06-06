from django.db import models

class Story(models.Model):
    narration = models.TextField()
    options = models.JSONField()
    image_prompt = models.TextField()

    def __str__(self):
        return f"Story: {self.narration[:50]}..."
