from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class CycleLog(models.Model):
    """Tracks each menstrual cycle period start/end."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycle_logs')
    period_start_date = models.DateField()
    period_end_date = models.DateField(null=True, blank=True)
    cycle_length = models.IntegerField(null=True, blank=True, help_text="Days from this period start to next period start")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-period_start_date']
        unique_together = ['user', 'period_start_date']

    def __str__(self):
        return f"{self.user.username} - {self.period_start_date}"

    @property
    def period_length(self):
        if self.period_end_date:
            return (self.period_end_date - self.period_start_date).days + 1
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_previous_cycle_length()

    def _update_previous_cycle_length(self):
        previous = CycleLog.objects.filter(
            user=self.user,
            period_start_date__lt=self.period_start_date
        ).first()
        if previous:
            previous.cycle_length = (self.period_start_date - previous.period_start_date).days
            CycleLog.objects.filter(pk=previous.pk).update(
                cycle_length=(self.period_start_date - previous.period_start_date).days
            )


PAIN_LOCATIONS = [
    ('lower_abdomen', 'Lower Abdomen / Cramps'),
    ('lower_back', 'Lower Back'),
    ('headache', 'Headache / Migraine'),
    ('breast', 'Breast Tenderness'),
    ('joints', 'Joint Pain'),
    ('legs', 'Leg Pain / Cramps'),
    ('pelvis', 'Pelvic Pain'),
    ('full_body', 'Full Body Aches'),
    ('other', 'Other'),
]

FLOW_LEVELS = [
    ('none', 'None'),
    ('spotting', 'Spotting'),
    ('light', 'Light'),
    ('medium', 'Medium'),
    ('heavy', 'Heavy'),
    ('very_heavy', 'Very Heavy'),
]

MOOD_CHOICES = [
    (1, 'Very Low'),
    (2, 'Low'),
    (3, 'Okay'),
    (4, 'Good'),
    (5, 'Great'),
]

ENERGY_CHOICES = [
    (1, 'Exhausted'),
    (2, 'Low Energy'),
    (3, 'Normal'),
    (4, 'Energized'),
    (5, 'Very Energized'),
]


class Symptom(models.Model):
    """Predefined symptoms users can track."""
    CATEGORY_CHOICES = [
        ('pain', 'Pain & Discomfort'),
        ('physical', 'Physical'),
        ('emotional', 'Emotional'),
        ('digestive', 'Digestive'),
        ('skin', 'Skin & Hair'),
        ('sleep', 'Sleep'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class DailyLog(models.Model):
    """Daily tracking of symptoms, pain, mood, and flow."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()

    # Pain tracking (the core focus)
    pain_level = models.IntegerField(
        default=0,
        choices=[(i, str(i)) for i in range(11)],
        help_text="Pain level from 0 (none) to 10 (severe)"
    )
    pain_locations = models.JSONField(
        default=list, blank=True,
        help_text="List of pain location keys"
    )

    # Flow tracking
    flow_level = models.CharField(max_length=20, choices=FLOW_LEVELS, default='none')

    # Mood and energy
    mood = models.IntegerField(choices=MOOD_CHOICES, default=3)
    energy = models.IntegerField(choices=ENERGY_CHOICES, default=3)

    # Symptoms
    symptoms = models.ManyToManyField(Symptom, blank=True, related_name='daily_logs')

    # Physical metrics
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True,
        help_text="Basal body temperature in Fahrenheit"
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True,
        help_text="Weight in lbs"
    )
    water_intake = models.IntegerField(
        default=0, help_text="Glasses of water"
    )
    sleep_hours = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True,
        help_text="Hours of sleep"
    )
    exercise_minutes = models.IntegerField(default=0, help_text="Minutes of exercise")

    # Pain management
    pain_remedies = models.JSONField(
        default=list, blank=True,
        help_text="List of remedies tried today"
    )
    remedy_effectiveness = models.IntegerField(
        null=True, blank=True,
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text="How effective were your remedies? 1-5"
    )

    # Notes
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class PainRemedy(models.Model):
    """Tracks pain remedies and their effectiveness over time."""
    REMEDY_CATEGORIES = [
        ('medication', 'Medication'),
        ('heat', 'Heat Therapy'),
        ('exercise', 'Exercise / Movement'),
        ('rest', 'Rest'),
        ('nutrition', 'Nutrition / Diet'),
        ('herbal', 'Herbal / Natural'),
        ('massage', 'Massage'),
        ('breathing', 'Breathing / Meditation'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pain_remedies')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=REMEDY_CATEGORIES)
    description = models.TextField(blank=True)
    times_used = models.IntegerField(default=0)
    total_effectiveness = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-times_used']
        unique_together = ['user', 'name']
        verbose_name_plural = 'Pain Remedies'

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    @property
    def avg_effectiveness(self):
        if self.times_used > 0:
            return round(self.total_effectiveness / self.times_used, 1)
        return 0


class CyclePrediction(models.Model):
    """Stores predictions for upcoming cycles."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cycle_predictions')
    predicted_start = models.DateField()
    predicted_end = models.DateField()
    predicted_ovulation = models.DateField(null=True, blank=True)
    fertile_window_start = models.DateField(null=True, blank=True)
    fertile_window_end = models.DateField(null=True, blank=True)
    confidence_score = models.FloatField(default=0.0, help_text="0.0 to 1.0")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['predicted_start']

    def __str__(self):
        return f"{self.user.username} - Predicted: {self.predicted_start}"


class ReminderPreference(models.Model):
    """User preferences for period reminders."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reminder_prefs')
    days_before_period = models.IntegerField(default=3, help_text="Days before predicted period to send reminder")
    remind_via_email = models.BooleanField(default=True)
    daily_log_reminder = models.BooleanField(default=True, help_text="Remind to log daily symptoms")
    daily_reminder_time = models.TimeField(default='20:00', help_text="What time to send daily reminder")
    pain_tips_enabled = models.BooleanField(default=True, help_text="Receive personalized pain management tips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s reminder preferences"


class PartnerShare(models.Model):
    """Allow sharing cycle info with a partner."""
    SHARE_LEVELS = [
        ('dates_only', 'Period Dates Only'),
        ('dates_symptoms', 'Dates + General Symptoms'),
        ('everything', 'Full Details'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares_given')
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares_received')
    share_level = models.CharField(max_length=20, choices=SHARE_LEVELS, default='dates_only')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'partner']

    def __str__(self):
        return f"{self.user.username} shares with {self.partner.username}"
