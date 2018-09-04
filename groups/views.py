from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group,GroupMember
from . import models
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from posts.models import Post
from emoji_picker.widgets import EmojiPickerTextInput, EmojiPickerTextarea
from django import forms
from posts.forms import PostForm
from .forms import GroupForm
from notify.signals import notify

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    """
    Create group
    """
    form_class = GroupForm
    model = Group

    def form_valid(self, form):
        group = form.save()
        p1= Post.objects.create(group=group, message="Welcome to new group", user_id=1)
        p1.save()
        print(p1)
        return redirect("groups:all")

def upload_pic(request, post_id):
    """
    Upload picture in post
   :param request: 
    :param post_id: 
    :return: 
  """
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'post_pic' in request.FILES:
                form.post_pic = request.FILES['post_pic']
            m = get_object_or_404(Post, pk=post_id)
            m.post_pic = form.cleaned_data['post_pic']
            m.save()

class SingleGroup(FormMixin, generic.DetailView):
    """
    redrict to a group page
    """
    model = Group
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        #new post in group
        self.object = self.get_object()
        form = self.get_form()
        if request.method == 'POST':
            if form.is_valid():
                if 'post_pic' in request.FILES:
                    form.post_pic = request.FILES['post_pic']
                message = form.cleaned_data.get("message")
                new_post = Post.objects.create(group=self.object, message=message, user=request.user)
                upload_pic(request, new_post.id)
                return HttpResponseRedirect( self.object.get_absolute_url())

class ListGroups(generic.ListView):
    """
    List of All the Groups
    """
    model = Group

def get_members(request, slug):
    """ all the members of the group
    :param request:
    :param slug:
    :return: HttpResponse
    """
    group = Group.objects.get(slug=slug)
    members_list = GroupMember.objects.filter(group=group)
    args = { 'members_list' : members_list, 'group' : group}
    return render (request, 'groups/users_in_group.html', args)





class GetGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    """
    Join the group
    """
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        """get group obj"""
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
        #Join the group and create notification for all the group members
            followers = []
            for user in GroupMember.objects.filter(group=group):
                followers.append(user.user)
            notify.send(request.user, recipient_list=followers, actor=request.user,
                        verb = 'start followed ', nf_type = 'followed_by_one_user', target=group)
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    #leave group
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)

