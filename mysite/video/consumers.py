from channels.generic.websocket import AsyncJsonWebsocketConsumer


class VideoChat(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        if (content['command'] == 'join_room'):
            await self.channel_layer.group_add(content['room'], self.channel_name)
            print('added')

            await self.channel_layer.send(self.channel_name, {
                "type": "test.message"
            })
            # {'type':'join.message', 'count': content['room']})
        elif (content['command'] == 'join'):
            await self.channel_layer.group_send(content['room'], {
                'type': 'join.message',
            })

        elif (content['command'] == 'offer'):
            await self.channel_layer.group_send(content['room'], {
                'type': 'offer.message',
                'offer': content['offer'],
                'uuid': content['uuid'],
            })
        elif (content['command'] == 'answer'):
            await self.channel_layer.group_send(content['room'], {
                'type': 'answer.message',
                'answer': content['answer'],
                'uuid': content['uuid'],
            })
        elif (content['command'] == 'candidate'):
            await self.channel_layer.group_send(content['room'], {
                'type': 'candidate.message',
                'candidate': content['candidate'],
                'uuid': content['uuid'],
                # 'iscreated':content['iscreated']
            })
        elif (content['command'] == 'send_message'):
            print(content['message'])
            await self.channel_layer.group_send(content['room'], {
                'type': 'update.message',
                'message': content['message']
            })

    async def test_message(self, event):
        await self.send_json({
            'command': 'test',
        })

    async def join_message(self, event):
        await self.send_json({
            'command': 'join'
        })

    async def update_message(self, event):
        await self.send_json({
            'command': 'update_message',
            'message': event['message']
        })

    async def offer_message(self, event):
        await self.send_json({
            'command': 'offer',
            'offer': event['offer'],
            'uuid': event['uuid']
        })

    async def answer_message(self, event):
        await self.send_json({
            'command': 'answer',
            'answer': event['answer'],
            'uuid': event['uuid']
        })

    async def candidate_message(self, event):
        await self.send_json({
            'command': 'candidate',
            'candidate': event['candidate'],
            'uuid': event['uuid']
            # 'iscreated':event['iscreated']
        })