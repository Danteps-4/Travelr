from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from .models import ChatGroup, GroupMessage

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.user = self.scope["user"]
            self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"]
            self.chatroom = ChatGroup.objects.get(name=self.chatroom_name)

            async_to_sync(self.channel_layer.group_add)(
                self.chatroom_name, self.channel_name
            )

            # add and update online users
            if self.user not in self.chatroom.users_online.all():
                self.chatroom.users_online.add(self.user)
                self.update_online_count()

            self.accept()
        except ChatGroup.DoesNotExist:
            self.close()
        except Exception as e:
            print("ERROR EN CONNECT:", e)
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )
        # remove and update online users
        if self.user in self.chatroom.users_online.all():
            self.chatroom.users_online.remove(self.user)
            self.update_online_count()
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["body"]
        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )
        
        event = {
            "type": "message_handler",
            "message_id": message.id,
        }
        

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def message_handler(self, event):
        message_id = event["message_id"]
        message = GroupMessage.objects.get(id=message_id)
        context = {
            "message": message,
            "user": self.user,
        }
        html = render_to_string("chat/partials/chat_message_p.html", context=context)
        # print(html)
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count() - 1
        event = {
            "type": "online_count_handler",
            "online_count": online_count,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def online_count_handler(self, event):
        online_count = event["online_count"]
        context = {
            "online_count": online_count
        }
        html = render_to_string("chat/partials/online_count.html", context=context)
        self.send(text_data=html)