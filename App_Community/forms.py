from django import forms
from .models import AnonymousStory, StoryComment, StoryCategory


class AnonymousStoryForm(forms.ModelForm):
    class Meta:
        model = AnonymousStory
        fields = ['category', 'title', 'content', 'anonymous_name', 'age_at_experience']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Give your story a title...'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 8,
                'placeholder': 'Share your experience... This is a safe space. Your identity is hidden.'
            }),
            'anonymous_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Anonymous (or any name you choose)',
                'value': 'Anonymous'
            }),
            'age_at_experience': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 8, 'max': 100,
                'placeholder': 'Optional'
            }),
        }


class StoryCommentForm(forms.ModelForm):
    class Meta:
        model = StoryComment
        fields = ['content', 'anonymous_name']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Share words of support or your own experience...'
            }),
            'anonymous_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Anonymous',
                'value': 'Anonymous'
            }),
        }
