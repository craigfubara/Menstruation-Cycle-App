from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import CycleLog, DailyLog, PainRemedy, Symptom
from .prediction_engine import get_cycle_stats, get_current_cycle_day, get_current_phase


class CycleLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_cycle_log(self):
        log = CycleLog.objects.create(
            user=self.user,
            period_start_date=date.today() - timedelta(days=28),
            period_end_date=date.today() - timedelta(days=23),
        )
        self.assertEqual(log.period_length, 6)
        self.assertEqual(str(log), f"testuser - {log.period_start_date}")

    def test_cycle_length_auto_calculation(self):
        CycleLog.objects.create(
            user=self.user,
            period_start_date=date.today() - timedelta(days=56),
            period_end_date=date.today() - timedelta(days=51),
        )
        CycleLog.objects.create(
            user=self.user,
            period_start_date=date.today() - timedelta(days=28),
            period_end_date=date.today() - timedelta(days=23),
        )
        first_cycle = CycleLog.objects.filter(user=self.user).last()
        self.assertEqual(first_cycle.cycle_length, 28)


class PredictionEngineTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_no_data_returns_defaults(self):
        stats = get_cycle_stats(self.user)
        self.assertEqual(stats['avg_cycle_length'], 28)
        self.assertEqual(stats['total_cycles'], 0)

    def test_current_cycle_day_no_data(self):
        self.assertIsNone(get_current_cycle_day(self.user))

    def test_current_phase_no_data(self):
        self.assertIsNone(get_current_phase(self.user))

    def test_current_cycle_day_with_data(self):
        CycleLog.objects.create(
            user=self.user,
            period_start_date=date.today() - timedelta(days=5),
        )
        self.assertEqual(get_current_cycle_day(self.user), 6)

    def test_current_phase_menstrual(self):
        CycleLog.objects.create(
            user=self.user,
            period_start_date=date.today() - timedelta(days=2),
        )
        phase = get_current_phase(self.user)
        self.assertEqual(phase['phase'], 'menstrual')


class TrackerViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_dashboard_loads(self):
        response = self.client.get(reverse('App_Tracker:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_log_period_get(self):
        response = self.client.get(reverse('App_Tracker:log_period'))
        self.assertEqual(response.status_code, 200)

    def test_log_period_post(self):
        response = self.client.post(reverse('App_Tracker:log_period'), {
            'period_start_date': date.today().isoformat(),
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CycleLog.objects.filter(user=self.user).count(), 1)

    def test_daily_log_get(self):
        response = self.client.get(reverse('App_Tracker:daily_log'))
        self.assertEqual(response.status_code, 200)

    def test_pain_management_loads(self):
        response = self.client.get(reverse('App_Tracker:pain_management'))
        self.assertEqual(response.status_code, 200)

    def test_cycle_history_loads(self):
        response = self.client.get(reverse('App_Tracker:cycle_history'))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('App_Tracker:dashboard'))
        self.assertEqual(response.status_code, 302)


class PainRemedyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_remedy_avg_effectiveness(self):
        remedy = PainRemedy.objects.create(
            user=self.user,
            name='Heating pad',
            category='heat',
            times_used=3,
            total_effectiveness=12,
        )
        self.assertEqual(remedy.avg_effectiveness, 4.0)

    def test_remedy_no_uses(self):
        remedy = PainRemedy.objects.create(
            user=self.user,
            name='New remedy',
            category='other',
        )
        self.assertEqual(remedy.avg_effectiveness, 0)
