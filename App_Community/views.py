from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import F

from .models import AnonymousStory, StoryCategory, StoryReaction, StoryComment
from .forms import AnonymousStoryForm, StoryCommentForm


def story_list(request):
    """Browse all approved anonymous stories."""
    categories = StoryCategory.objects.all()
    stories = AnonymousStory.objects.filter(is_approved=True)

    # Filter by category
    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(StoryCategory, slug=category_slug)
        stories = stories.filter(category=active_category)

    # Sort
    sort = request.GET.get('sort', 'recent')
    if sort == 'me_too':
        stories = stories.order_by('-me_too_count', '-created_at')
    elif sort == 'support':
        stories = stories.order_by('-support_count', '-created_at')
    else:
        stories = stories.order_by('-created_at')

    paginator = Paginator(stories, 12)
    page = request.GET.get('page')
    stories = paginator.get_page(page)

    context = {
        'stories': stories,
        'categories': categories,
        'active_category': active_category,
        'sort': sort,
    }
    return render(request, 'App_Community/story_list.html', context)


def story_detail(request, slug):
    """Read a single anonymous story with comments."""
    story = get_object_or_404(AnonymousStory, slug=slug, is_approved=True)
    comments = story.comments.filter(is_approved=True)
    comment_form = StoryCommentForm()

    user_reactions = []
    if request.user.is_authenticated:
        user_reactions = list(
            StoryReaction.objects.filter(story=story, user=request.user)
            .values_list('reaction_type', flat=True)
        )

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = StoryCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.story = story
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('App_Community:story_detail', slug=slug)

    context = {
        'story': story,
        'comments': comments,
        'comment_form': comment_form,
        'user_reactions': user_reactions,
    }
    return render(request, 'App_Community/story_detail.html', context)


@login_required
def share_story(request):
    """Share a new anonymous story."""
    if request.method == 'POST':
        form = AnonymousStoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            if not story.anonymous_name:
                story.anonymous_name = 'Anonymous'
            story.save()
            messages.success(request, 'Your story has been shared! Thank you for your courage.')
            return redirect('App_Community:story_detail', slug=story.slug)
    else:
        form = AnonymousStoryForm()

    context = {'form': form}
    return render(request, 'App_Community/share_story.html', context)


@login_required
@require_POST
def react_to_story(request, pk, reaction_type):
    """Add or remove a reaction (me_too or support) on a story."""
    story = get_object_or_404(AnonymousStory, pk=pk)

    if reaction_type not in ('me_too', 'support'):
        messages.error(request, 'Invalid reaction.')
        return redirect('App_Community:story_detail', slug=story.slug)

    existing = StoryReaction.objects.filter(
        story=story, user=request.user, reaction_type=reaction_type
    )

    if existing.exists():
        existing.delete()
        if reaction_type == 'me_too':
            AnonymousStory.objects.filter(pk=pk).update(me_too_count=F('me_too_count') - 1)
        else:
            AnonymousStory.objects.filter(pk=pk).update(support_count=F('support_count') - 1)
    else:
        StoryReaction.objects.create(
            story=story, user=request.user, reaction_type=reaction_type
        )
        if reaction_type == 'me_too':
            AnonymousStory.objects.filter(pk=pk).update(me_too_count=F('me_too_count') + 1)
        else:
            AnonymousStory.objects.filter(pk=pk).update(support_count=F('support_count') + 1)

    return redirect('App_Community:story_detail', slug=story.slug)
