from django.contrib import admin
from .models import (
    CycleLog, DailyLog, Symptom, PainRemedy,
    CyclePrediction, ReminderPreference, PartnerShare
)


@admin.register(CycleLog)
class CycleLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'period_start_date', 'period_end_date', 'cycle_length']
    list_filter = ['user', 'period_start_date']
    search_fields = ['user__username']


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'pain_level', 'flow_level', 'mood', 'energy']
    list_filter = ['user', 'date', 'flow_level']
    search_fields = ['user__username']


@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon']
    list_filter = ['category']


@admin.register(PainRemedy)
class PainRemedyAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'category', 'times_used', 'avg_effectiveness']
    list_filter = ['category']


@admin.register(CyclePrediction)
class CyclePredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'predicted_start', 'predicted_end', 'confidence_score', 'is_active']
    list_filter = ['is_active', 'user']


@admin.register(ReminderPreference)
class ReminderPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'days_before_period', 'remind_via_email', 'daily_log_reminder']


@admin.register(PartnerShare)
class PartnerShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'partner', 'share_level', 'is_active']
    list_filter = ['share_level', 'is_active']
