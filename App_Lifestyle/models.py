from django.db import models


class LifestyleTip(models.Model):
    """Phase-specific lifestyle recommendations focused on pain and comfort."""
    PHASE_CHOICES = [
        ('menstrual', 'Menstrual Phase'),
        ('follicular', 'Follicular Phase'),
        ('ovulation', 'Ovulation Phase'),
        ('luteal', 'Luteal Phase'),
        ('all', 'All Phases'),
    ]
    CATEGORY_CHOICES = [
        ('pain_relief', 'Pain Relief'),
        ('exercise', 'Exercise & Movement'),
        ('nutrition', 'Nutrition'),
        ('self_care', 'Self Care'),
        ('sleep', 'Sleep'),
        ('mental_health', 'Mental Health'),
        ('work_life', 'Work & Productivity'),
    ]

    phase = models.CharField(max_length=20, choices=PHASE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fas fa-heart')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['phase', 'order']

    def __str__(self):
        return f"{self.get_phase_display()} - {self.title}"
