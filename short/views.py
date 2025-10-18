from django.shortcuts import render, redirect
from django.views.generic import CreateView, View, ListView
from .models import Short
# from .forms import BlogForm, CommentForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

#
# class CreateBlogView(CreateView, LoginRequiredMixin):
#     """
#     View to create blog article
#     """
#     model = Blog
#     template_name = "blog/create.html"
#     form_class = BlogForm
#
#     # save authenticated user if form is valid
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


class ShortListView(ListView):
    """
    View for all blog list
    """
    model = Short
    context_object_name = "shorts"
    template_name = "short/list.html"


# class BlogDetailView(View):
#     """
#     View for blog detail
#     """
#     def get(self, *args, **kwargs):
#         slug = kwargs.get('slug')
#         blog = Blog.objects.get(slug=slug)
#         context = {
#             'form': CommentForm(self.request.POST),
#             'blog': blog
#         }
#         return render(self.request, 'blog/detail.html', context)
#
#     def post(self, request, *args, **kwargs):
#         slug = kwargs.get('slug')
#         blog = Blog.objects.get(slug=slug)
#         if request.method == "POST":
#             form = CommentForm(request.POST)
#             if form.is_valid:
#                 comment = form.save(commit=False)
#                 comment.author = request.user
#                 comment.post = blog
#                 comment.save()
#                 return redirect(blog.get_absolute_url())
#
#
# def like(request, slug):
#     blog = Blog.objects.get(slug=slug)
#     if request.method == "POST":
#         blog.likes.add(request.user)
#         blog.save()
#         return redirect(blog.get_absolute_url())
