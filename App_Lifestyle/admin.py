from django.contrib import admin
from .models import LifestyleTip


@admin.register(LifestyleTip)
class LifestyleTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'phase', 'category', 'order']
    list_filter = ['phase', 'category']
    search_fields = ['title', 'description']
