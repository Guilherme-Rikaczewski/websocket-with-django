from channels.generic.websocket import AsyncWebsocketConsumer
import json
from urllib.parse import parse_qs
from .utils import rgb_generator


class AuthenticatedEchoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('conect chamado')
        user = self.scope["user"]

        query_string = self.scope.get('query_string', b'').decode('utf-8')
        query_params = parse_qs(query_string)

        if user.is_anonymous:
            await self.close()
            return

        self.group_name = query_params.get('room', None)[0]

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        await self.send_user_joined()
        
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

    # HANDLER
    async def broadcast_message(self, event):
        await self.send(text_data=json.dumps({
            'user': event['user'],
            'data': event['data']
        }))

    async def send_user_joined(self,):
        user = self.scope['user']
        r, g, b = rgb_generator()
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'broadcast_message',
                'user': user.username,
                'data': {
                    'type': 'user_joined',
                    # retorna uma tupla com valroes aleatorios para (r, g, b)
                    'color': f'rgb({r},{g},{b})',
                }
            }
        )
