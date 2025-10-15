from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, ListView
from .models import Blog
from .forms import BlogForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class CreateBlogView(CreateView, LoginRequiredMixin):
    """
    View to create blog article
    """
    model = Blog
    template_name = "blog/create.html"
    form_class = BlogForm
    #
    # def get_success_url(self):
    #     return reverse(self.object.get_detail())

    # save authenticated user if form is valid
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogListView(ListView):
    """
    View for all blog list
    """
    model = Blog
    context_object_name = "blogs"
    template_name = "blog/list.html"

    # Queryset to render all blog from db in order of publish_date (newest first)
    def get_queryset(self):
        return Blog.objects.order_by('-publish_date')


class BlogDetailView(View):
    """
    View for blog detail
    """
    def get(self, slug, *args, **kwargs):
        blog = Blog.objects.get(slug=slug)
        context = {
            # 'form': CommentForm(self.request.POST),
            'blog': blog
        }
        return render(self.request, 'blog/detail.html', context)

    # def post(self, request, slug, *args, **kwargs):
    #     blog = Blog.objects.get(title=title, slug=slug)
    #     if request.method == "POST":
    #         form = CommentForm(request.POST)
    #         if form.is_valid:
    #             comment = form.save(commit=False)
    #             comment.author = request.user
    #             comment.post = blog
    #             comment.save()
    #             return redirect(blog.get_detail())
