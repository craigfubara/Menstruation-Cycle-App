"""
Cycle prediction engine for menstrual cycle forecasting.
Uses historical cycle data to predict future periods, ovulation, and fertile windows.
"""
from datetime import timedelta, date
from django.db.models import Avg, StdDev

DEFAULT_CYCLE_LENGTH = 28
DEFAULT_PERIOD_LENGTH = 5
MIN_CYCLES_FOR_PREDICTION = 2


def get_cycle_stats(user):
    """Calculate cycle statistics from user's history."""
    from App_Tracker.models import CycleLog

    cycles = CycleLog.objects.filter(
        user=user,
        cycle_length__isnull=False
    ).values_list('cycle_length', flat=True)

    cycle_lengths = list(cycles)
    if not cycle_lengths:
        return {
            'avg_cycle_length': DEFAULT_CYCLE_LENGTH,
            'avg_period_length': DEFAULT_PERIOD_LENGTH,
            'std_dev': 0,
            'total_cycles': 0,
            'confidence': 0.0,
            'shortest_cycle': None,
            'longest_cycle': None,
        }

    # Period lengths
    periods = CycleLog.objects.filter(
        user=user,
        period_end_date__isnull=False
    )
    period_lengths = []
    for p in periods:
        pl = (p.period_end_date - p.period_start_date).days + 1
        if 1 <= pl <= 15:
            period_lengths.append(pl)

    avg_period = sum(period_lengths) / len(period_lengths) if period_lengths else DEFAULT_PERIOD_LENGTH

    avg_cycle = sum(cycle_lengths) / len(cycle_lengths)
    n = len(cycle_lengths)

    if n >= 2:
        variance = sum((x - avg_cycle) ** 2 for x in cycle_lengths) / (n - 1)
        std_dev = variance ** 0.5
    else:
        std_dev = 0

    # Confidence: more cycles + lower variation = higher confidence
    cycle_confidence = min(n / 6, 1.0)  # Max at 6 cycles
    variation_confidence = max(0, 1.0 - (std_dev / 10))  # Penalize high std dev
    confidence = round((cycle_confidence * 0.6 + variation_confidence * 0.4), 2)

    return {
        'avg_cycle_length': round(avg_cycle, 1),
        'avg_period_length': round(avg_period, 1),
        'std_dev': round(std_dev, 1),
        'total_cycles': n,
        'confidence': confidence,
        'shortest_cycle': min(cycle_lengths),
        'longest_cycle': max(cycle_lengths),
    }


def predict_next_cycles(user, num_predictions=3):
    """Predict the next N cycles based on historical data."""
    from App_Tracker.models import CycleLog, CyclePrediction

    stats = get_cycle_stats(user)
    avg_cycle = round(stats['avg_cycle_length'])
    avg_period = round(stats['avg_period_length'])
    confidence = stats['confidence']

    # Get the most recent period
    last_cycle = CycleLog.objects.filter(user=user).first()
    if not last_cycle:
        return []

    # Deactivate old predictions
    CyclePrediction.objects.filter(user=user, is_active=True).update(is_active=False)

    predictions = []
    base_date = last_cycle.period_start_date

    for i in range(1, num_predictions + 1):
        predicted_start = base_date + timedelta(days=avg_cycle * i)
        predicted_end = predicted_start + timedelta(days=avg_period - 1)

        # Ovulation typically ~14 days before next period
        predicted_ovulation = predicted_start + timedelta(days=avg_cycle - 14)
        fertile_start = predicted_ovulation - timedelta(days=5)
        fertile_end = predicted_ovulation + timedelta(days=1)

        prediction = CyclePrediction.objects.create(
            user=user,
            predicted_start=predicted_start,
            predicted_end=predicted_end,
            predicted_ovulation=predicted_ovulation,
            fertile_window_start=fertile_start,
            fertile_window_end=fertile_end,
            confidence_score=confidence,
            is_active=True,
        )
        predictions.append(prediction)

    return predictions


def get_current_cycle_day(user):
    """Calculate what day of the current cycle the user is on."""
    from App_Tracker.models import CycleLog

    last_cycle = CycleLog.objects.filter(user=user).first()
    if not last_cycle:
        return None

    today = date.today()
    cycle_day = (today - last_cycle.period_start_date).days + 1
    return cycle_day


def get_current_phase(user):
    """Determine what phase of the cycle the user is in."""
    cycle_day = get_current_cycle_day(user)
    if cycle_day is None:
        return None

    stats = get_cycle_stats(user)
    avg_cycle = stats['avg_cycle_length']
    avg_period = stats['avg_period_length']

    if cycle_day <= avg_period:
        return {
            'phase': 'menstrual',
            'name': 'Menstrual Phase',
            'description': 'Your period is happening. Focus on rest, warmth, and gentle care.',
            'day': cycle_day,
            'color': '#e74c3c',
        }
    elif cycle_day <= avg_cycle * 0.45:
        return {
            'phase': 'follicular',
            'name': 'Follicular Phase',
            'description': 'Energy is rising! Great time for new projects and social activities.',
            'day': cycle_day,
            'color': '#2ecc71',
        }
    elif cycle_day <= avg_cycle * 0.55:
        return {
            'phase': 'ovulation',
            'name': 'Ovulation Phase',
            'description': 'Peak energy and confidence. Your body is at its most fertile.',
            'day': cycle_day,
            'color': '#f39c12',
        }
    else:
        return {
            'phase': 'luteal',
            'name': 'Luteal Phase',
            'description': 'Energy may dip. Practice self-compassion and prepare for your period.',
            'day': cycle_day,
            'color': '#9b59b6',
        }


def get_pain_insights(user):
    """Analyze pain patterns and provide insights."""
    from App_Tracker.models import DailyLog, CycleLog

    logs = DailyLog.objects.filter(user=user, pain_level__gt=0).order_by('-date')[:90]

    if not logs:
        return {
            'avg_pain': 0,
            'worst_days': [],
            'best_remedies': [],
            'pain_pattern': 'Not enough data yet. Keep logging!',
            'total_pain_days': 0,
        }

    pain_levels = [log.pain_level for log in logs]
    avg_pain = sum(pain_levels) / len(pain_levels)

    # Find which cycle days have worst pain
    pain_by_cycle_day = {}
    for log in logs:
        last_period = CycleLog.objects.filter(
            user=user,
            period_start_date__lte=log.date
        ).first()
        if last_period:
            day = (log.date - last_period.period_start_date).days + 1
            if day not in pain_by_cycle_day:
                pain_by_cycle_day[day] = []
            pain_by_cycle_day[day].append(log.pain_level)

    worst_days = sorted(
        [(day, sum(pains) / len(pains)) for day, pains in pain_by_cycle_day.items()],
        key=lambda x: x[1],
        reverse=True
    )[:5]

    # Find most effective remedies
    from App_Tracker.models import PainRemedy
    best_remedies = PainRemedy.objects.filter(
        user=user,
        times_used__gte=2
    ).order_by('-total_effectiveness')[:5]

    # Determine pain pattern
    if avg_pain >= 7:
        pattern = "Your pain levels are consistently high. Consider consulting a healthcare provider about managing severe menstrual pain."
    elif avg_pain >= 4:
        pattern = "You experience moderate pain during your cycles. The remedies that work best for you are showing in your data."
    else:
        pattern = "Your pain levels are generally manageable. Keep tracking to identify any changes."

    return {
        'avg_pain': round(avg_pain, 1),
        'worst_days': worst_days,
        'best_remedies': list(best_remedies),
        'pain_pattern': pattern,
        'total_pain_days': len(pain_levels),
    }
