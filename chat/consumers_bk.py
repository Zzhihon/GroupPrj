# chat/consumers.py
import json
from django.core.serializers.json import DjangoJSONEncoder
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from asgiref.sync import sync_to_async
from demo.models import Profile,ChatRoom,Message
from demo.serializers import MessageSerializer
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode('utf-8')
        params = parse_qs(query_string)
        token = params.get('token',[None])[0]
        result = await self.auth_token(token)

        if not result:
            return
        
        await self.join_chat_room()
        await self.fetch_message()
        


    async def disconnect(self, close_code):
        # Leave room group
        await self.leave_chat_room()

    # Receive message from WebSocket
    async def receive(self, text_data):
        # 转换格式
        text_data_json = json.loads(text_data)

        # 消息的具体信息
        message = text_data_json.get("message",None)
        # 消息的类型
        message_type = text_data_json.get("message_type",None)
        # 目标用户的id
        target_user = text_data_json.get("target_user",None)
        # 目标聊天室
        target_room = text_data_json.get("target_room",None)
        
        
        # 发送给用户的信息
        if message_type=="chat" and target_user and target_room:
                await self.save_message_recode(target_room,self.user,message)
                await self.channel_layer.group_send(
                    str(target_room),{
                        "type":"chat.message",
                        "message":{
                            "sender_name":self.user.username,
                            "chat_room":target_room,
                            "content":message
                        }
                    }
                )
        # 加入聊天室的信息
        elif message_type=="join" and target_user:
            user_group = f"user_{target_user}"

            roomId = await self.launch_chat(target_user)

            if roomId and roomId!='fail' and roomId != 'exist':
                await self.channel_layer.group_send(
                    user_group,{
                        "type":"join.message",
                        "message":{
                            "group_id":roomId,
                            "user":self.user.username
                        }
                    }
                )
                await self.send(text_data=json.dumps({
                    "type":"success",
                    "code":1,
                    "detail":"chatroom create"
                },cls=DjangoJSONEncoder))
            elif roomId == 'exist':
                await self.send(text_data=json.dumps({
                    "type":"error",
                    "code":1,
                    "detail":"chatroom exist"
                },cls=DjangoJSONEncoder))
            elif roomId == 'fail':
                await self.send(text_data=json.dumps({
                    "type":"error",
                    "code":2,
                    "detail":"create fail"
                },cls=DjangoJSONEncoder))


    async def chat_message(self, event):
        """接受聊天信息"""
        # event["type"] = "chat"
        # 向客户端发送
        await self.send(text_data=json.dumps({
                "type":"chat",
                **event["message"]
            },cls=DjangoJSONEncoder))

    async def join_message(self, event):
        """通知其他用户"""
        event["message"]["type"] = "join"

        await self.send(text_data=json.dumps(event["message"],cls=DjangoJSONEncoder))

    async def log_in_message(self, event):
        event["message"]["type"] = "login"

        await self.send(text_data=json.dumps(event["message"],cls=DjangoJSONEncoder))

    async def auth_token(self,token):
        """验证用户的身份"""
        if token:
            jwt_auth = JWTAuthentication()
            try:
                validated_token = jwt_auth.get_validated_token(token)
                user = await sync_to_async(jwt_auth.get_user)(validated_token)
                self.user = user
                await self.accept()
                return True
            except Exception as e:
                self.user = AnonymousUser()
                await self.close()
                return False
        else:
            self.user = AnonymousUser()
            await self.close()
            return False

    async def join_chat_room(self):
        """读取用户相关聊天室,并自动加入"""

        # 首先加入以自己user_id命名组,保证可以直接找到
        await self.channel_layer.group_add(
            f"user_{self.user.id}",
            self.channel_name
        )

        chatrooms = await self.get_rooms_by_user(self.user)
        self.chatrooms = dict()

        # 向前端提供所有的聊天室
        respone_message = []

        for chatroom in chatrooms:
            # 加入到group
            await self.channel_layer.group_add(
                str(chatroom.id),
                self.channel_name
            )
            # 寻找另一个用户
            another_user = await self.get_user_by_room(chatroom)
            self.chatrooms[another_user.id] = chatroom
            await self.channel_layer.group_send(
                f"user_{another_user.id}",
                {
                    "type":"log.in.message",
                    "message":{
                        "room":chatroom.id,
                        "user":self.user.username
                    }
                }
            )
            respone_message.append({"user":another_user.username,"roomid":chatroom.id})
        
        await self.send(text_data=json.dumps({
            "type":"room_message",
            "message":respone_message
        },cls=DjangoJSONEncoder))

    async def leave_chat_room(self):
        """离开聊天室"""
        if hasattr(self,"chatrooms"):
            for chatroom in self.chatrooms.values():
                await self.channel_layer.group_discard(
                    str(chatroom.id),
                    self.channel_name
                )

    async def launch_chat(self,target_userid):
        # 创建聊天室方法
        roomid = await self.create_chat_room([self.user.id,target_userid])
        if roomid == 'fail' or roomid == 'exist':
            return roomid
        await self.channel_layer.group_add(
            str(roomid),
            self.channel_name
        )

        return roomid

    async def fetch_message(self):
        """同步聊天记录"""
        pass
        recodes = await self.get_message_recode(self.user)

        await self.send(text_data=json.dumps({
            "type":"fetch",
            "message":recodes
        },cls=DjangoJSONEncoder))

    # 数据库操作
    @sync_to_async
    def get_rooms_by_user(self,user: User):
        return list(user.chat_rooms.all())
    
    @sync_to_async
    def get_user_by_room(self,chatroom:ChatRoom):
        return chatroom.participants.exclude(id=self.user.id).first()
    
    @sync_to_async
    def save_message_recode(self,chatroom:ChatRoom,user:User,message:str):
        # 整合数据
        message_data = {
            'chat_room':chatroom,
            'sender':str(user.id),
            'content':message
        }

        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()
            return True
        return False

    @sync_to_async
    def select_user_by_userid(self,userid):
        return User.objects.get(id=userid)
    
    @sync_to_async
    def create_chat_room(self,participants):
        data = {
            'participants':participants
        }
        try:
            serializer = ChatRoomSerializer(data=data)
            if serializer.is_valid():
                chatroom = serializer.save()
                return chatroom.id
        except IntegrityError:
            return "exist"
        return "fail"
    
    @sync_to_async
    def get_message_recode(self,user:User):
        message_recode_in_chatrooms = []
        
        for chatroom in self.chatrooms.values():
            messages = chatroom.message_set.all()
            serializer = MessageSerializer(messages,many=True)
            message_recode_in_chatrooms.append({
                "chatroom":chatroom.id,
                "message":serializer.data
            })
        
        return message_recode_in_chatrooms
