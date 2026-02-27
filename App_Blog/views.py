from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, TemplateView, DeleteView
from App_Blog.models import Blog, Comment, Likes
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.http import Http404
import uuid
from App_Blog.forms import CommentForm


class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/my_blogs.html'


class UpdateBlog(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_content', 'blog_image')
    template_name = 'App_Blog/edit_blog.html'

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author

    def get_success_url(self, **kwargs):
        return reverse_lazy('App_Blog:blog_details', kwargs={'slug': self.object.slug})


class DeleteBlog(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'App_Blog/confirm_delete.html'
    success_url = reverse_lazy('App_Blog:my_blogs')

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'
    queryset = Blog.objects.order_by('-public_date')
    paginate_by = 10


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'App_Blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image')

    def form_valid(self, form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        blog_obj.slug = slugify(blog_obj.blog_title) + "-" + str(uuid.uuid4())[:8]
        blog_obj.save()
        return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug': blog_obj.slug}))


def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comment_form = CommentForm()
    liked = False

    if request.user.is_authenticated:
        already_liked = Likes.objects.filter(blog=blog, user=request.user)
        if already_liked.exists():
            liked = True

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('App_Login:signin'))
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug': slug}))

    return render(request, 'App_Blog/blog_details.html', context={
        'blog': blog,
        'comment_form': comment_form,
        'liked': liked,
    })


@login_required
@require_POST
def liked(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    if not already_liked.exists():
        Likes.objects.create(blog=blog, user=user)
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug': blog.slug}))


@login_required
@require_POST
def unliked(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user
    Likes.objects.filter(blog=blog, user=user).delete()
    return HttpResponseRedirect(reverse('App_Blog:blog_details', kwargs={'slug': blog.slug}))
