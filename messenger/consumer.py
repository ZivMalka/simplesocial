import asyncio
import json

from channels.consumer import SyncConsumer, AsyncConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        """websocekt connect"""
        print("connected", event)
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        #thread_obj to create new message
        self.thread_obj = thread_obj
        await self.channel_layer.group_add(chat_room, self.channel_name)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        """websocekt receive"""
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_data = json.loads(front_text)
            msg =loaded_data.get('message')
            user = self.scope['user']
            username = 'default'
            if  user.is_authenticated:
                username = user.username
                await self.insert_obj_to_databae(user, msg)
            my_Response = {
                'message' : msg,
                'username':username
            }
            await self.channel_layer.group_send(self.chat_room,{"type" : "chat_message","text": json.dumps(my_Response)})

    async def chat_message(self, event):
        print('message', event)
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        """return the therad obj"""
        print("ee")
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def insert_obj_to_databae(self, me, msg):
        """create new chat message"""
        thread_obj = self.thread_obj
        new_message = ChatMessage.objects.create(
            thread= thread_obj,
            user=me,
            message=msg
        )
