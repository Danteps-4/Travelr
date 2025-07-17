from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    # path("view/", views.chat_view, name="chat_view"),
    path("user/<slug:slug>", views.get_or_create_chatroom, name="chat_user"),
    path("user/room/<chatroom_name>", views.chat_view, name="chatroom"),
    path("new-groupchat/", views.create_groupchat, name="new_groupchat"),
    path("room/edit/<chatroom_name>", views.chatroom_edit, name="edit_chatroom"),
    path("room/delete/<chatroom_name>", views.chatroom_delete, name="delete_chatroom"),
    path("room/leave/<chatroom_name>", views.chatroom_leave, name="leave_chatroom"),
]
