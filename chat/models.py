import shortuuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatGroup(models.Model):
    name = models.CharField(max_length=255, unique=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="groupchats", blank=True, null=True)
    users_online = models.ManyToManyField(User, related_name="online_in_groups", blank=True)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name="chat_messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.body}"
    
    class Meta:
        ordering = ["-created"]