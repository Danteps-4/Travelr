from django.forms import ModelForm
from django import forms

from .models import GroupMessage, ChatGroup

class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]

class NewGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["groupchat_name"]

class EditChatroomForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ["groupchat_name"]