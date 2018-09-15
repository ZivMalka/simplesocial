from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView
from django.urls import reverse
from .forms import ComposeForm
from .models import Thread, ChatMessage
from notify.signals import notify

class InboxView(LoginRequiredMixin, ListView):
    """return messeges list of the user"""
    template_name = 'messenger/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['users_list'] = get_user_model().objects.filter(
            is_active=True).exclude(
            username=self.request.user).order_by('username')
      #  last_conversation = Thread.objects.get_most_recent_conversation(
       #     self.request.user
        #)
        return context


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'messenger/messenger.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['users_list'] = get_user_model().objects.filter(
            is_active=True).exclude(
            username=self.request.user).order_by('username')
        last_conversation = Thread.objects.get_most_recent_conversation(
            self.request.user
        )
        context['other_user']  = get_user_model().objects.get(username=self.kwargs["username"])
        context['active'] = last_conversation.username
        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        new_message = ChatMessage.objects.create(user=user, thread=thread, message=message)
        notify.send(user, recipient=thread.second, actor=user, verb='Send you a new message.',
                    nf_type='message_by_one_user', target=new_message)

        return super().form_valid(form)


class ConversationListView(ThreadView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['active'] = self.kwargs["username"]
        return context

    def get_queryset(self):
        active_user = get_user_model().objects.get(username=self.kwargs["username"])
        return Thread.objects.get_or_new(active_user, self.request.user)