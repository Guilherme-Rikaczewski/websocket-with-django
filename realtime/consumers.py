from channels.generic.websocket import AsyncWebsocketConsumer
import json


class AuthenticatedEchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('conect chamado')
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
            return

        self.group_name = 'global'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print(f'WebSocket conectado {user.username}')

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("Desconectando")
        return await super().disconnect(code)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_message',
                'user': user.username,
                'data': data,
            }
        )

    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            'user': event['user'],
            'data': event['data']
        }))
