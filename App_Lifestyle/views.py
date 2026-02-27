from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .recommendations import get_all_recommendations


@login_required
def recommendations(request):
    """Show cycle-synced lifestyle recommendations based on current phase."""
    from App_Tracker.prediction_engine import get_current_phase, get_current_cycle_day, get_cycle_stats

    current_phase = get_current_phase(request.user)
    cycle_day = get_current_cycle_day(request.user)
    stats = get_cycle_stats(request.user)

    if current_phase:
        phase_key = current_phase['phase']
    else:
        phase_key = None

    all_recs = get_all_recommendations(phase_key)

    context = {
        'current_phase': current_phase,
        'cycle_day': cycle_day,
        'stats': stats,
        'recommendations': all_recs,
        'phase_key': phase_key,
    }
    return render(request, 'App_Lifestyle/recommendations.html', context)
