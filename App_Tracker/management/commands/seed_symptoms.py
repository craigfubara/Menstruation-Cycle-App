from django.core.management.base import BaseCommand
from App_Tracker.models import Symptom


SYMPTOMS = [
    # Pain & Discomfort
    ('Cramps', 'pain', 'fas fa-bolt'),
    ('Lower Back Pain', 'pain', 'fas fa-bone'),
    ('Headache', 'pain', 'fas fa-head-side-virus'),
    ('Migraine', 'pain', 'fas fa-brain'),
    ('Breast Tenderness', 'pain', 'fas fa-hand-holding-heart'),
    ('Joint Pain', 'pain', 'fas fa-bone'),
    ('Leg Cramps', 'pain', 'fas fa-shoe-prints'),
    ('Pelvic Pressure', 'pain', 'fas fa-compress-arrows-alt'),

    # Physical
    ('Bloating', 'physical', 'fas fa-circle'),
    ('Fatigue', 'physical', 'fas fa-battery-quarter'),
    ('Nausea', 'physical', 'fas fa-dizzy'),
    ('Dizziness', 'physical', 'fas fa-spinner'),
    ('Hot Flashes', 'physical', 'fas fa-thermometer-full'),
    ('Chills', 'physical', 'fas fa-snowflake'),
    ('Increased Appetite', 'physical', 'fas fa-utensils'),
    ('Decreased Appetite', 'physical', 'fas fa-utensils'),
    ('Water Retention', 'physical', 'fas fa-tint'),
    ('Weight Gain', 'physical', 'fas fa-weight'),

    # Emotional
    ('Mood Swings', 'emotional', 'fas fa-theater-masks'),
    ('Irritability', 'emotional', 'fas fa-angry'),
    ('Anxiety', 'emotional', 'fas fa-heartbeat'),
    ('Sadness', 'emotional', 'fas fa-sad-tear'),
    ('Crying Spells', 'emotional', 'fas fa-sad-cry'),
    ('Sensitivity', 'emotional', 'fas fa-heart'),
    ('Low Motivation', 'emotional', 'fas fa-couch'),
    ('Brain Fog', 'emotional', 'fas fa-cloud'),

    # Digestive
    ('Constipation', 'digestive', 'fas fa-minus-circle'),
    ('Diarrhea', 'digestive', 'fas fa-exclamation-circle'),
    ('Gas', 'digestive', 'fas fa-wind'),
    ('Food Cravings', 'digestive', 'fas fa-cookie-bite'),

    # Skin & Hair
    ('Acne', 'skin', 'fas fa-dot-circle'),
    ('Oily Skin', 'skin', 'fas fa-tint'),
    ('Dry Skin', 'skin', 'fas fa-sun'),
    ('Hair Loss', 'skin', 'fas fa-cut'),

    # Sleep
    ('Insomnia', 'sleep', 'fas fa-moon'),
    ('Oversleeping', 'sleep', 'fas fa-bed'),
    ('Night Sweats', 'sleep', 'fas fa-moon'),
    ('Vivid Dreams', 'sleep', 'fas fa-star'),
]


class Command(BaseCommand):
    help = 'Seed the database with predefined symptoms'

    def handle(self, *args, **options):
        created_count = 0
        for name, category, icon in SYMPTOMS:
            _, created = Symptom.objects.get_or_create(
                name=name,
                defaults={'category': category, 'icon': icon}
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} symptoms ({len(SYMPTOMS)} total)')
        )
