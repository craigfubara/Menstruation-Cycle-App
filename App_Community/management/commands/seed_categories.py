from django.core.management.base import BaseCommand
from App_Community.models import StoryCategory


CATEGORIES = [
    {
        'name': 'First Period Stories',
        'slug': 'first-period',
        'description': 'Share your first period experience. Every story helps someone feel less alone.',
        'icon': 'fas fa-star',
        'color': '#e74c3c',
        'order': 1,
    },
    {
        'name': 'Pain & Discomfort',
        'slug': 'pain-discomfort',
        'description': 'Stories about managing period pain, cramps, and physical discomfort.',
        'icon': 'fas fa-first-aid',
        'color': '#9b59b6',
        'order': 2,
    },
    {
        'name': 'PCOS/PCOD Journeys',
        'slug': 'pcos-journeys',
        'description': 'Living with PCOS or PCOD. Diagnosis stories, treatment journeys, and daily life.',
        'icon': 'fas fa-ribbon',
        'color': '#2ecc71',
        'order': 3,
    },
    {
        'name': 'Workplace & School',
        'slug': 'workplace-school',
        'description': 'Managing periods at work or school. The challenges and how you handled them.',
        'icon': 'fas fa-briefcase',
        'color': '#3498db',
        'order': 4,
    },
    {
        'name': 'Cultural Experiences',
        'slug': 'cultural',
        'description': 'How different cultures and families handle menstruation. Breaking taboos.',
        'icon': 'fas fa-globe',
        'color': '#f39c12',
        'order': 5,
    },
    {
        'name': 'Tips That Actually Work',
        'slug': 'tips-that-work',
        'description': 'Remedies, products, and life hacks that genuinely helped your period experience.',
        'icon': 'fas fa-lightbulb',
        'color': '#1abc9c',
        'order': 6,
    },
    {
        'name': 'Emotional Journey',
        'slug': 'emotional',
        'description': 'The emotional side of menstruation. PMS, mood changes, and mental health.',
        'icon': 'fas fa-heart',
        'color': '#e91e63',
        'order': 7,
    },
]


class Command(BaseCommand):
    help = 'Seed the database with story categories'

    def handle(self, *args, **options):
        created = 0
        for cat_data in CATEGORIES:
            _, was_created = StoryCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data,
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Created {created} categories ({len(CATEGORIES)} total)')
        )
