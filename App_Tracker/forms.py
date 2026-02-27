from django import forms
from .models import CycleLog, DailyLog, PainRemedy, ReminderPreference, PartnerShare, PAIN_LOCATIONS


class CycleLogForm(forms.ModelForm):
    period_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="When did your period start?"
    )
    period_end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        label="When did it end? (leave blank if ongoing)"
    )

    class Meta:
        model = CycleLog
        fields = ['period_start_date', 'period_end_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Any notes about this cycle...'}),
        }


class DailyLogForm(forms.ModelForm):
    pain_location_choices = forms.MultipleChoiceField(
        choices=PAIN_LOCATIONS,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Where is the pain?"
    )

    class Meta:
        model = DailyLog
        fields = [
            'pain_level', 'flow_level', 'mood', 'energy',
            'temperature', 'sleep_hours', 'exercise_minutes',
            'water_intake', 'notes',
        ]
        widgets = {
            'pain_level': forms.NumberInput(attrs={
                'type': 'range', 'min': 0, 'max': 10, 'step': 1,
                'class': 'form-range', 'id': 'painSlider'
            }),
            'flow_level': forms.Select(attrs={'class': 'form-select'}),
            'mood': forms.Select(attrs={'class': 'form-select'}),
            'energy': forms.Select(attrs={'class': 'form-select'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '98.6'}),
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': '8'}),
            'exercise_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'water_intake': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'How are you feeling today?'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['pain_location_choices'].initial = self.instance.pain_locations

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.pain_locations = self.cleaned_data.get('pain_location_choices', [])
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class PainRemedyForm(forms.ModelForm):
    class Meta:
        model = PainRemedy
        fields = ['name', 'category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Heating pad on lower back'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Describe how you use this remedy...'}),
        }


class RemedyEffectivenessForm(forms.Form):
    remedy = forms.ModelChoiceField(
        queryset=PainRemedy.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Which remedy did you try?"
    )
    effectiveness = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'type': 'range', 'min': 1, 'max': 5, 'step': 1,
            'class': 'form-range'
        }),
        label="How effective was it? (1=Not at all, 5=Very effective)"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['remedy'].queryset = PainRemedy.objects.filter(user=user)


class ReminderPreferenceForm(forms.ModelForm):
    class Meta:
        model = ReminderPreference
        fields = ['days_before_period', 'remind_via_email', 'daily_log_reminder',
                  'daily_reminder_time', 'pain_tips_enabled']
        widgets = {
            'days_before_period': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 14}),
            'daily_reminder_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }


class PartnerShareForm(forms.Form):
    partner_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Partner username'}),
        label="Partner's Username"
    )
    share_level = forms.ChoiceField(
        choices=PartnerShare.SHARE_LEVELS,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="What to share"
    )
