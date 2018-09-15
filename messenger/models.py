from django.db import models
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

class ThreadManager(models.Manager):
    def by_user(self, user):
        """return user conversation"""
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_most_recent_conversation(self, recipient):
        """Returns the most recent conversation counterpart's username."""
        try:
            qs_sent = self.filter(first=recipient)
            qs_recieved = self.filter(second=recipient)
            qs = qs_sent.union(qs_recieved).latest("timestamp")
            if qs.first == recipient:
                return qs.second

            return qs.first

        except self.model.DoesNotExist:
            return get_user_model().objects.get(username=recipient.username)

    def mark_conversation_as_read(self, sender, recipient):
        """Mark as read any unread elements in the current conversation."""
        qs = self.filter(sender=sender, recipient=recipient)
        return qs.update(unread=False)

    def get_or_new(self, user, other_username):  # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                    first=user,
                    second=user2
                )

                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    """thears obj"""
    first = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    """chat obj"""
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse("messenger:conversation_detail", kwargs={"username": self.user})