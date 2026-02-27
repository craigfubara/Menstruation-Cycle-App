from django.contrib import admin
from .models import StoryCategory, AnonymousStory, StoryReaction, StoryComment


@admin.register(StoryCategory)
class StoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'story_count']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AnonymousStory)
class AnonymousStoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'anonymous_name', 'me_too_count', 'support_count', 'is_approved', 'created_at']
    list_filter = ['category', 'is_approved', 'is_reported']
    search_fields = ['title', 'content']
    actions = ['approve_stories', 'reject_stories']

    def approve_stories(self, request, queryset):
        queryset.update(is_approved=True)
    approve_stories.short_description = "Approve selected stories"

    def reject_stories(self, request, queryset):
        queryset.update(is_approved=False)
    reject_stories.short_description = "Reject selected stories"


@admin.register(StoryComment)
class StoryCommentAdmin(admin.ModelAdmin):
    list_display = ['story', 'anonymous_name', 'is_approved', 'created_at']
    list_filter = ['is_approved']
