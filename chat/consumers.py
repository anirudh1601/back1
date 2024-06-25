import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import base64
from .serializers import UserSerializer
from django.core.files.base import ContentFile

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        # print(user,user.is_authenticated)
        if not user.is_authenticated:
            return
        
        self.username = user.username

        async_to_sync(self.channel_layer.group_add)(
            self.username,self.channel_name
        )

        self.accept()
        print('connected')  

    def disconnect(self, close_code):
        user = self.scope['user']
        self.username = user.username
        async_to_sync(self.channel_layer.group_discard)(
            self.username,self.channel_name
        )


    def receive(self, text_data):

        data = json.loads(text_data)


        message = data.get("source")
        print('receive', json.dumps(data, indent=2))

        if message == "thumbnail":
            self.receive_thumbnail(data)

        self.send(text_data=json.dumps({"message": 'message'}))

    
    def receive_thumbnail(self,data):
        user = self.scope['user']

        image_str = data['base64']
        image = ContentFile(base64.b64decode(image_str))

        filename = data.get('filename')

        user.thumbnail.save(filename,image,save=True)

        serialized = UserSerializer(user)

        self.send_group(self.username,'thumbnail',serialized.data)


    def send_group(self,group,source,data):
        response = {
            'type':'broadcast_group',
            'source':source,
            'data':data
        }

        async_to_sync(self.channel_layer.group_send)(
            group,response
        )


    def broadcast_group(self,data):
        data.pop('type')
        self.send(text_data=json.dumps(data))