import json, uuid
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from demo.models import Profile,ChatRoom,Message,Trade
from demo.serializers import MessageSerializer
from django.contrib.auth.models import User
from django.conf import settings
from django.core.cache import cache

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):  #当前端通过我们刚刚写的链接试图与我们建立连接时我们会执行这个函数
        self.userid = self.scope['url_route']['kwargs']['userid']
        await self.channel_layer.group_add(str(self.userid), self.channel_name)
        await self.accept()  #建立连接


    async def disconnet(self, close_code):
        print("disconnect")
        await self.channel_layer.group_discard(self.uuid, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data['event']

        if event == 'fetchallchatrooms':
            chatroomidlist = await self.fetchallchatroomid(str(data['userid'])) #获取所有tradeid,一个tradeid对应一个聊天室
            chatroomlist = await self.getchatroomlist(data['userid']) #返回的是一个嵌套字典的列表[{'seller': seller_username, 'buyer':buyer_username,'item': item_name},]
            await self.addtogroups(chatroomidlist) #将用户group_add到他所拥有的chatroom中
            await self.channel_layer.group_send(
                self.userid,
                {
                    'type': 'fetch_allchatrooms',
                    'event': 'fetchchatroomlist',
                    'chatroomlist': chatroomlist
                    }
            )

        if event == 'sendnotice':
            buyer = await self.getmyusername(self.userid)
            await self.channel_layer.group_send(
                str(data['another_userid']),
                {
                    'type': 'send_notice',
                    'event': 'sendnotice',
                    'content': f'{buyer}正向你发起聊天'
                }
            )

        if event == 'sendmessage':
            await self.savemessage(data)
            sender = await self.getmyusername(self.userid)
            await self.channel_layer.group_send(
                str(data['tradeid']),
                {
                    'type': 'send_message',
                    'event': 'sendmessage',
                    'sender': sender,
                    'content': data['content']
                }
            )

        if event == 'fetchmessage':
            history_messages = await self.getmessage(data['tradeid'])
            await self.channel_layer.group_send(
                str(data['tradeid']),
                {
                    'type': 'fetch_message',
                    'event': 'fetchmessage',
                    'history_messages': history_messages
                }
            )

    async def addtogroups(self, chatroomidlist):
        for chatroomid in chatroomidlist:
            await self.channel_layer.group_add(str(chatroomid), self.channel_name)

    async def fetch_allchatrooms(self, data):
        await self.send(text_data=json.dumps(data))

    async def send_notice(self, data):
        await self.send(text_data=json.dumps(data))

    async def send_message(self, data):
        await self.send(text_data=json.dumps(data))

    async def fetch_message(self, data):
        await self.send(text_data=json.dumps(data))

    @sync_to_async
    def fetchallchatroomid(self, userid):
        profile = Profile.objects.get(id=userid)
        trades_seller = profile.seller.all()
        trades_buyer = profile.buyer.all()
        tradelist = []
        for trade in trades_seller:
            tradeid = trade.id
            tradelist.append(tradeid)
        for trade in trades_buyer:
            tradeid = trade.id
            tradelist.append(tradeid)
        
        return tradelist
        
    @sync_to_async
    def getchatroomlist(self, userid):
        profile = Profile.objects.get(id=userid)
        trades_seller = profile.seller.all()
        trades_buyer = profile.buyer.all()
        chatroomlist = []
        for trade in trades_seller:
            buyer_username = trade.buyer.username
            chatroomlist.append({'seller':profile.username, 'buyer':buyer_username,'item': trade.item.name})
        for trade in trades_buyer:
            seller_username = trade.seller.username
            chatroomlist.append({'seller':seller_username, 'buyer':profile.username,'item':trade.item.name})

        return chatroomlist
        
    @sync_to_async
    def getmyusername(self, userid):
        profile = Profile.objects.get(id=userid)
        my_username = profile.username
        return my_username

    @sync_to_async
    def savemessage(self, data):
        trade = Trade.objects.get(id=data['tradeid'])
        sender = Profile.objects.get(id=data['userid'])
        content = data['content']
        message = Message.objects.create(trade=trade, sender=sender, content=content)
        
    @sync_to_async
    def getmessage(self, tradeid):
        trade = Trade.objects.get(id=tradeid)
        messages = trade.message_set.all()
        history_messages = []
        for message in messages:
            sender = message.sender
            history_messages.append({'sender':sender.username, 'content':message.content})

        return history_messages





