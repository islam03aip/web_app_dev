from django.db import models


class Book(models.Model):
    class Status(models.TextChoices):
        TO_READ = "to_read", "To read"
        READING = "reading", "Reading"
        FINISHED = "finished", "Finished"

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TO_READ)
    rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="1-5, optional")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} by {self.author}"
