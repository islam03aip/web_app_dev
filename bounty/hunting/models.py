from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class WantedCriminal(models.Model):
    name = models.CharField(max_length=200, blank=True, default="",
                            help_text="Real name; blank if unknown.")
    nickname = models.CharField(max_length=200)
    reward = models.DecimalField(max_digits=14, decimal_places=2,
                                 validators=[MinValueValidator(0)])
    latitude = models.FloatField(null=True, blank=True,
                                 validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(null=True, blank=True,
                                  validators=[MinValueValidator(-180), MaxValueValidator(180)])
    last_known_note = models.TextField(blank=True, default="",
                                       help_text="Free-text note about the last known location.")
    difficulty = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    armed = models.BooleanField(default=False)
    has_crew = models.BooleanField(default=False)
    escape_master = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.nickname} ({self.reward})"


class HuntLog(models.Model):
    criminal = models.ForeignKey(WantedCriminal, on_delete=models.CASCADE,
                                 related_name="hunts")
    success = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Hunt #{self.pk} for {self.criminal_id} ({'captured' if self.success else 'failed'})"
