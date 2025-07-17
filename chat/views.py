from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from .models import ChatGroup, GroupMessage
from .forms import ChatMessageCreateForm, NewGroupForm, EditChatroomForm
from account.models import Profile

# Create your views here.
@login_required
def chat_view(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:30]

    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
    
    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)

    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                "message": message,
                "user": request.user,
            }
            return render(request, "chat/partials/chat_message_p.html", context)

    context = {"group": chat_group, "chat_messages": chat_messages, "form": form, "other_user": other_user, "chatroom_name": chatroom_name, "chat_group": chat_group}
    return render(request, "chat/chat.html", context)

@login_required
def get_or_create_chatroom(request, slug):
    if request.user.profile.slug == slug:
        return redirect("account:profile_view", slug=request.user.profile.slug)
    
    other_user = Profile.objects.get(slug=slug).user
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect("chat:chatroom", chatroom.name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()

    if request.method == "POST":
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect("chat:chatroom", new_groupchat.name)

    context = {"form": form}
    return render(request, "chat/create_groupchat.html", context)

@login_required
def chatroom_edit(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    form = EditChatroomForm(instance=chat_group)

    if request.method == "POST":
        form = EditChatroomForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save()
            remove_members = request.POST.getlist("remove_members")
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)

            return redirect("chat:chatroom", chatroom_name)
        
    context = {"form": form, "chat_group": chat_group}
    return render(request, "chat/chatroom_edit.html", context)

@login_required
def chatroom_delete(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == "POST":
        chat_group.delete()
        messages.success(request, "Chatroom deleted")
        return redirect("account:profile_view", request.user.profile.slug)
    
    context = {"chat_group": chat_group}
    return render(request, "chat/chatroom_delete.html", context)

@login_required
def chatroom_leave(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, name=chatroom_name)
    if request.user not in chat_group.members.all():
        raise Http404()
    
    if request.method == "POST":
        chat_group.members.remove(request.user)
        messages.success(request, "You left the chat")
        return redirect("account:profile_view", request.user.profile.slug)