import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
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
from posts.models import Post, Like
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
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import datetime
from posts.decorators import ajax_required
from notify.signals import notify
class SingleGroup(generic.DetailView):
    model = Group


class PostList(SelectRelatedMixin, generic.ListView):
    '''return the feed'''
    model = models.Post
    select_related = ("user", "group")


class UserPosts(generic.ListView):
    '''return user posts list'''
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        '''find all user posts'''
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
           
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        '''return post list of the user'''
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")


    def get_category__slug(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    '''delete'''
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
        obj = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        url_ = obj.get_posts_url()
        user = self.request.user
        if user in obj.likes.all():
            obj.likes.remove(user)


        else:
            obj.likes.add(user)
            obj.date_of_like = datetime.datetime.now()

        return url_


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeAPIToggle(APIView):
    """CREATE lIKE USING API REST FRAMWORK
     ajax response
    """
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        url_ = obj.get_posts_url()
        user = self.request.user
        updated = False
        liked = False
        user_like  = Like.objects.filter(post=obj, user=user)
        if user_like:
                liked = False
                user_like.delete()
                #obj.likes.remove(user)
        else:
                liked = True
                #obj.likes.add(user)
                Like.objects.create(user=user, post=obj)
                notify.send(request.user, recipient=obj.user, actor=request.user, verb='Like your post.',
                    nf_type='liked_by_one_user', target=obj)
        updated = True
        data = {
            "updated": updated,
            "liked": liked
        }


        return Response(data)



@csrf_exempt
def comment(request):
    """
    new comment
    :param request:
    ajax response
    """
    if request.method == 'POST':

        print("S")
        post_id = request.POST.get('post_id')
        print(post_id)
        post = Post.objects.get(pk=post_id)
        content = request.POST.get('content')
        user = request.user

        response_data = {}
        new_comment = Comment.objects.create(content_object=post, content=content, user=request.user)

        #notifications
        notify.send(request.user, recipient=post.user, actor=request.user, verb='comment on your post.',
                    nf_type='comment_by_one_user', target=post)

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = new_comment.pk
        response_data['text'] = new_comment.content
        response_data['created'] = new_comment.timestamp.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = new_comment.user.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


