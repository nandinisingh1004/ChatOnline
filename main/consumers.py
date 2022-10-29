import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer
from .models import PersonalChats, Friends
from usergroups.models import Groups, GroupChats, GroupUsers
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname = self.scope['url_route']['kwargs']['groupname']
        self.room_group_name = 'chat_%s' % self.groupname
        self.group = await self.groupFind()
        self.user = self.scope['user']
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        msgtype = text_data_json['type']
        if(msgtype == 1):
            await self.saveGroupChats(message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message, 
                'user' : self.user.username,
                'msg_type' : msgtype
            }
        )
        

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']
        msgtype = event['msg_type']
        # Send message to WebSocket
        await self.send(text_data = json.dumps({
            'message': message,
            'sender' : user,
            'msg_type' : msgtype
        }))

    @database_sync_to_async
    def saveGroupChats(self, message):
        obj = GroupChats(sender = self.user, group = self.group, chats = message)
        obj.save()
    @database_sync_to_async
    def groupFind(self):
        return Groups.objects.get(groupname = self.groupname)

class PersonalChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        person1 = self.scope['url_route']['kwargs']['otheruser']
        self.person2 = self.scope['user'].username
        self.arr = [person1, self.person2]
        self.arr.sort()
        self.room_group_name = self.arr[0] + 'talks' + self.arr[1]
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.send({
            'type' : 'websocket.accept'
        })

    async def websocket_receive(self, event):
        data = event.get('text', None)
        if data is not None:
            msg_data = json.loads(data)
            message = msg_data['message']
            senttype = msg_data['type']
            if(senttype == 1):
                await self.savePersonalChats(message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type' : 'personalchat.message',
                    'message' : message,
                    'sender' : self.person2,
                    'msg_type' : senttype
                }
            )
            
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def personalchat_message(self, event):
        message = event['message']
        sender = event['sender']
        msg_type = event['msg_type']
        await self.send({
            'type' : 'websocket.send',
            'text' : json.dumps({
                'message' : message,
                'sender' : sender,
                'msg_type' : msg_type
            })
        })

    @database_sync_to_async
    def savePersonalChats(self, message):
        p = PersonalChats(friend = Friends.objects.get(owner__username = self.arr[0], friend__username = self.arr[1]), chat = message, sender = self.person2)
        p.save()