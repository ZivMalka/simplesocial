
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.views import generic
from groups.models import Group
from braces.views import SelectRelatedMixin
from . import forms
from . import models
from posts.models import Post
from .forms import PostForm
from activities.models import Comment
from activities.forms import CommentForm
from .models import Post
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import RedirectView


from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.shortcuts import get_object_or_404
from django.views import generic
from django.db.models import Q

from django.contrib.contenttypes.models import ContentType


class SingleGroup(generic.DetailView):
    model = Group


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ("user", "group")





class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )



def writePost(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(data=request.POST)
            if form.is_valid():
                message = form.cleaned_data.get("message")


                if 'post_pic' in request.FILES:
                    profile.profile_pic = request.FILES['post_pic']

                Post.objects.create(group=group, message=message , user=request.user)

            return HttpResponseRedirect(reverse("posts:single_2" , kwargs={"slug": group.slug}))
        else:
            form = PostForm()

        return render(request, 'posts/post_form.html', {'form': form})


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group', 'post_pic')
    model = models.Post

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        if 'post_pic' in request.FILES:
            self.object.profile_pic = request.FILES['post_pic']


        return super().form_valid(form)



def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
   # post = Post.objects.get(pk=1)

    if request.method == "POST":
            form = CommentForm(data=request.POST)
            if form.is_valid():

                content_data = form.cleaned_data.get("content")

                Comment.objects.create(content_object=post, content=content_data, user=request.user)

            return HttpResponseRedirect(post.get_posts_url())
    else:
        form = CommentForm()

    return render(request, 'posts/partial_feed_comment.html', {'form': form})



class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)




class like(RedirectView, LoginRequiredMixin):

    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Post, slug=self.kwargs.get("slug"))
        url_ = obj.get_posts_url()
        user = self.request.user
        if user in obj.likes.all():
            obj.likes.remove(user)
        else:
            obj.likes.add(user)

        return url_




