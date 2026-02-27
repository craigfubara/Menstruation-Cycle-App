from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
import json

from .models import (
    CycleLog, DailyLog, Symptom, PainRemedy, CyclePrediction,
    ReminderPreference, PartnerShare
)
from .forms import (
    CycleLogForm, DailyLogForm, PainRemedyForm,
    RemedyEffectivenessForm, ReminderPreferenceForm, PartnerShareForm
)
from .prediction_engine import (
    get_cycle_stats, predict_next_cycles, get_current_cycle_day,
    get_current_phase, get_pain_insights
)


@login_required
def dashboard(request):
    """Main tracker dashboard with cycle overview, pain summary, and predictions."""
    today = date.today()
    stats = get_cycle_stats(request.user)
    current_phase = get_current_phase(request.user)
    cycle_day = get_current_cycle_day(request.user)
    pain_insights = get_pain_insights(request.user)

    # Get today's log if exists
    today_log = DailyLog.objects.filter(user=request.user, date=today).first()

    # Get active predictions
    predictions = CyclePrediction.objects.filter(
        user=request.user, is_active=True, predicted_start__gte=today
    )[:3]

    # Next predicted period
    next_prediction = predictions.first() if predictions else None
    days_until_period = None
    if next_prediction:
        days_until_period = (next_prediction.predicted_start - today).days

    # Recent logs for the chart
    recent_logs = DailyLog.objects.filter(
        user=request.user,
        date__gte=today - timedelta(days=30)
    ).order_by('date')

    # Chart data
    chart_dates = [log.date.strftime('%b %d') for log in recent_logs]
    chart_pain = [log.pain_level for log in recent_logs]
    chart_mood = [log.mood for log in recent_logs]

    # Recent cycle logs
    cycle_logs = CycleLog.objects.filter(user=request.user)[:6]

    context = {
        'stats': stats,
        'current_phase': current_phase,
        'cycle_day': cycle_day,
        'pain_insights': pain_insights,
        'today_log': today_log,
        'predictions': predictions,
        'next_prediction': next_prediction,
        'days_until_period': days_until_period,
        'recent_logs': recent_logs,
        'chart_dates': json.dumps(chart_dates),
        'chart_pain': json.dumps(chart_pain),
        'chart_mood': json.dumps(chart_mood),
        'cycle_logs': cycle_logs,
        'today': today,
    }
    return render(request, 'App_Tracker/dashboard.html', context)


@login_required
def log_period(request):
    """Log a new period start/end."""
    if request.method == 'POST':
        form = CycleLogForm(request.POST)
        if form.is_valid():
            cycle = form.save(commit=False)
            cycle.user = request.user
            cycle.save()
            # Regenerate predictions
            predict_next_cycles(request.user)
            messages.success(request, 'Period logged successfully!')
            return redirect('App_Tracker:dashboard')
    else:
        form = CycleLogForm()
    return render(request, 'App_Tracker/log_period.html', {'form': form})


@login_required
def daily_log(request):
    """Log daily symptoms, pain, mood, etc."""
    today = date.today()
    existing_log = DailyLog.objects.filter(user=request.user, date=today).first()

    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=existing_log, user=request.user)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.date = today
            log.save()
            form.save_m2m()

            # Handle symptom selection
            symptom_ids = request.POST.getlist('symptoms')
            if symptom_ids:
                log.symptoms.set(symptom_ids)

            messages.success(request, "Today's log saved!")
            return redirect('App_Tracker:dashboard')
    else:
        form = DailyLogForm(instance=existing_log, user=request.user)

    symptoms = Symptom.objects.all().order_by('category', 'name')
    symptoms_by_category = {}
    for symptom in symptoms:
        cat = symptom.get_category_display()
        if cat not in symptoms_by_category:
            symptoms_by_category[cat] = []
        symptoms_by_category[cat].append(symptom)

    selected_symptoms = existing_log.symptoms.values_list('id', flat=True) if existing_log else []

    context = {
        'form': form,
        'existing_log': existing_log,
        'symptoms_by_category': symptoms_by_category,
        'selected_symptoms': list(selected_symptoms),
        'today': today,
    }
    return render(request, 'App_Tracker/daily_log.html', context)


@login_required
def pain_management(request):
    """Pain management hub - track remedies and see what works."""
    remedies = PainRemedy.objects.filter(user=request.user)
    pain_insights = get_pain_insights(request.user)

    if request.method == 'POST':
        if 'add_remedy' in request.POST:
            form = PainRemedyForm(request.POST)
            if form.is_valid():
                remedy = form.save(commit=False)
                remedy.user = request.user
                remedy.save()
                messages.success(request, f'Remedy "{remedy.name}" added!')
                return redirect('App_Tracker:pain_management')
        elif 'log_effectiveness' in request.POST:
            eff_form = RemedyEffectivenessForm(request.POST, user=request.user)
            if eff_form.is_valid():
                remedy = eff_form.cleaned_data['remedy']
                effectiveness = eff_form.cleaned_data['effectiveness']
                remedy.times_used += 1
                remedy.total_effectiveness += effectiveness
                remedy.save()
                messages.success(request, 'Effectiveness logged!')
                return redirect('App_Tracker:pain_management')

    remedy_form = PainRemedyForm()
    effectiveness_form = RemedyEffectivenessForm(user=request.user)

    # Pain tips based on current phase
    current_phase = get_current_phase(request.user)
    pain_tips = get_phase_pain_tips(current_phase)

    context = {
        'remedies': remedies,
        'pain_insights': pain_insights,
        'remedy_form': remedy_form,
        'effectiveness_form': effectiveness_form,
        'current_phase': current_phase,
        'pain_tips': pain_tips,
    }
    return render(request, 'App_Tracker/pain_management.html', context)


def get_phase_pain_tips(phase):
    """Return pain management tips based on current cycle phase."""
    if not phase:
        return []

    tips = {
        'menstrual': [
            {'title': 'Heat Therapy', 'desc': 'Apply a heating pad to your lower abdomen or back. Heat relaxes uterine muscles and reduces cramping.', 'icon': 'fas fa-fire'},
            {'title': 'Gentle Movement', 'desc': 'Light walking or gentle yoga (child\'s pose, cat-cow) can ease cramps by boosting blood flow.', 'icon': 'fas fa-walking'},
            {'title': 'Anti-inflammatory Foods', 'desc': 'Ginger tea, turmeric, dark chocolate, and omega-3 rich foods can reduce inflammation.', 'icon': 'fas fa-mug-hot'},
            {'title': 'Hydration', 'desc': 'Drink warm water and herbal teas. Dehydration worsens cramps and bloating.', 'icon': 'fas fa-tint'},
            {'title': 'Rest & Breathe', 'desc': 'Deep breathing exercises and adequate rest help manage pain naturally.', 'icon': 'fas fa-lungs'},
            {'title': 'Magnesium', 'desc': 'Magnesium-rich foods (nuts, bananas, leafy greens) can help relax muscles and reduce cramps.', 'icon': 'fas fa-seedling'},
        ],
        'follicular': [
            {'title': 'Build Strength', 'desc': 'Energy is rising! Great time for more intense workouts that build pain resilience.', 'icon': 'fas fa-dumbbell'},
            {'title': 'Iron-Rich Foods', 'desc': 'Replenish iron lost during your period with spinach, red meat, lentils, and fortified cereals.', 'icon': 'fas fa-leaf'},
            {'title': 'Prepare Your Kit', 'desc': 'Stock up on pain relief supplies for next cycle: heating pad, herbal tea, medications.', 'icon': 'fas fa-first-aid'},
        ],
        'ovulation': [
            {'title': 'Stay Active', 'desc': 'Peak energy phase! Regular exercise now builds your pain tolerance for later.', 'icon': 'fas fa-running'},
            {'title': 'Mild Ovulation Pain', 'desc': 'Some women feel mild one-sided pain (mittelschmerz). This is normal and passes quickly.', 'icon': 'fas fa-info-circle'},
        ],
        'luteal': [
            {'title': 'Prevent PMS Pain', 'desc': 'Start gentle self-care now. Calcium and vitamin B6 can reduce PMS symptoms.', 'icon': 'fas fa-shield-alt'},
            {'title': 'Reduce Salt & Caffeine', 'desc': 'Both worsen bloating and breast tenderness. Switch to herbal teas.', 'icon': 'fas fa-ban'},
            {'title': 'Stress Management', 'desc': 'Stress amplifies pain perception. Try meditation, journaling, or warm baths.', 'icon': 'fas fa-spa'},
            {'title': 'Sleep Priority', 'desc': 'Aim for 8+ hours. Poor sleep worsens PMS pain and mood symptoms.', 'icon': 'fas fa-moon'},
        ],
    }
    return tips.get(phase['phase'], [])


@login_required
def cycle_history(request):
    """View all past cycles and logs."""
    cycles = CycleLog.objects.filter(user=request.user)
    stats = get_cycle_stats(request.user)

    context = {
        'cycles': cycles,
        'stats': stats,
    }
    return render(request, 'App_Tracker/cycle_history.html', context)


@login_required
def settings_view(request):
    """Tracker settings: reminders, partner sharing."""
    reminder_prefs, _ = ReminderPreference.objects.get_or_create(user=request.user)
    shares = PartnerShare.objects.filter(user=request.user, is_active=True)
    partner_views = PartnerShare.objects.filter(partner=request.user, is_active=True)

    if request.method == 'POST':
        if 'save_reminders' in request.POST:
            form = ReminderPreferenceForm(request.POST, instance=reminder_prefs)
            if form.is_valid():
                form.save()
                messages.success(request, 'Reminder preferences saved!')
                return redirect('App_Tracker:settings')

        elif 'add_partner' in request.POST:
            partner_form = PartnerShareForm(request.POST)
            if partner_form.is_valid():
                username = partner_form.cleaned_data['partner_username']
                share_level = partner_form.cleaned_data['share_level']
                try:
                    partner_user = User.objects.get(username=username)
                    if partner_user == request.user:
                        messages.error(request, "You can't share with yourself!")
                    else:
                        PartnerShare.objects.update_or_create(
                            user=request.user,
                            partner=partner_user,
                            defaults={'share_level': share_level, 'is_active': True}
                        )
                        messages.success(request, f'Now sharing with {username}!')
                except User.DoesNotExist:
                    messages.error(request, f'User "{username}" not found.')
                return redirect('App_Tracker:settings')

        elif 'remove_partner' in request.POST:
            share_id = request.POST.get('share_id')
            PartnerShare.objects.filter(pk=share_id, user=request.user).update(is_active=False)
            messages.success(request, 'Sharing removed.')
            return redirect('App_Tracker:settings')

    reminder_form = ReminderPreferenceForm(instance=reminder_prefs)
    partner_form = PartnerShareForm()

    context = {
        'reminder_form': reminder_form,
        'partner_form': partner_form,
        'shares': shares,
        'partner_views': partner_views,
    }
    return render(request, 'App_Tracker/settings.html', context)


@login_required
def calendar_data(request):
    """API endpoint for calendar view data."""
    user = request.user
    today = date.today()
    start = today - timedelta(days=90)
    end = today + timedelta(days=90)

    events = []

    # Period days
    cycles = CycleLog.objects.filter(
        user=user,
        period_start_date__gte=start
    )
    for cycle in cycles:
        end_date = cycle.period_end_date or (cycle.period_start_date + timedelta(days=4))
        events.append({
            'title': 'Period',
            'start': cycle.period_start_date.isoformat(),
            'end': (end_date + timedelta(days=1)).isoformat(),
            'color': '#e74c3c',
            'type': 'period',
        })

    # Predictions
    predictions = CyclePrediction.objects.filter(
        user=user, is_active=True, predicted_start__lte=end
    )
    for pred in predictions:
        events.append({
            'title': f'Predicted Period ({int(pred.confidence_score * 100)}%)',
            'start': pred.predicted_start.isoformat(),
            'end': (pred.predicted_end + timedelta(days=1)).isoformat(),
            'color': '#e74c3c',
            'type': 'prediction',
            'borderColor': '#c0392b',
            'opacity': 0.5,
        })
        if pred.fertile_window_start:
            events.append({
                'title': 'Fertile Window',
                'start': pred.fertile_window_start.isoformat(),
                'end': (pred.fertile_window_end + timedelta(days=1)).isoformat(),
                'color': '#2ecc71',
                'type': 'fertile',
            })
        if pred.predicted_ovulation:
            events.append({
                'title': 'Predicted Ovulation',
                'start': pred.predicted_ovulation.isoformat(),
                'color': '#f39c12',
                'type': 'ovulation',
            })

    # Pain levels from daily logs
    logs = DailyLog.objects.filter(user=user, date__gte=start, pain_level__gt=0)
    for log in logs:
        if log.pain_level >= 7:
            color = '#e74c3c'
        elif log.pain_level >= 4:
            color = '#f39c12'
        else:
            color = '#3498db'
        events.append({
            'title': f'Pain: {log.pain_level}/10',
            'start': log.date.isoformat(),
            'color': color,
            'type': 'pain',
        })

    return JsonResponse(events, safe=False)
