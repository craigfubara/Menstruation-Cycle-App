from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class StoryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-heart')
    color = models.CharField(max_length=7, default='#e74c3c')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Story Categories'

    def __str__(self):
        return self.name

    @property
    def story_count(self):
        return self.stories.filter(is_approved=True).count()


class AnonymousStory(models.Model):
    """Anonymous stories shared by community members. Author identity is hidden."""
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='anonymous_stories')
    anonymous_name = models.CharField(max_length=50, default='Anonymous', help_text="Display name (anonymous by default)")
    category = models.ForeignKey(StoryCategory, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=264)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    age_at_experience = models.IntegerField(null=True, blank=True, help_text="Your age when this happened (optional)")

    # Engagement
    me_too_count = models.IntegerField(default=0)
    support_count = models.IntegerField(default=0)

    # Moderation
    is_approved = models.BooleanField(default=True)
    is_reported = models.BooleanField(default=False)
    report_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Anonymous Stories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)


class StoryReaction(models.Model):
    """Track 'me too' and 'support' reactions (one per user per story)."""
    REACTION_TYPES = [
        ('me_too', 'Me Too'),
        ('support', 'Sending Support'),
    ]
    story = models.ForeignKey(AnonymousStory, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['story', 'user', 'reaction_type']

    def __str__(self):
        return f"{self.user.username} - {self.reaction_type} on {self.story.title}"


class StoryComment(models.Model):
    """Anonymous supportive comments on stories."""
    story = models.ForeignKey(AnonymousStory, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    anonymous_name = models.CharField(max_length=50, default='Anonymous')
    content = models.TextField(max_length=2000)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment on {self.story.title}"
