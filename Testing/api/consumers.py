import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

from .models import TestRoom, TestParticipant, Test

class TestRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Enhanced user authentication check
        if self.scope['user'].is_anonymous:
            await self.close(code=4001)  # Unauthorized
            return

        self.room_key = self.scope['url_route']['kwargs']['room_key']
        self.user = self.scope['user']
        self.room_group_name = f"test_room_{self.room_key}"
        
        if self.channel_layer is None:
            await self.close(code=4500)  # Internal server error
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        try:
            await self.handle_participant_join()
        except Exception as e:
            print(f"Error joining room: {e}")
            await self.close(code=4002)  # Custom error code

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.handle_participant_leave()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'ready':
            await self.mark_participant_ready()
        elif message_type == 'start_test':
            await self.start_test()
        elif message_type == 'submit_answer':
            await self.handle_answer_submission(data)

    @database_sync_to_async
    def handle_participant_join(self):
        if self.user.is_anonymous:
            raise ValueError("Authentication Failed; User is not authorized")
        
        room, _ = TestRoom.objects.get_or_create(
            room_key=self.room_key,
            defaults={'test' : Test.objects.first()}
        )

        user = self.user if not self.user.is_anonymous else None
        if not User:
            raise ValueError("Anonymous users cannot join the room")
    
        participant, created = TestParticipant.objects.get_or_create(
            user_id=user.id,
            room=room
        )

        return self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'participant_update',
                'participants': list(room.participants.values_list('user__email', flat=True))
            }
        )
    
    @database_sync_to_async
    def handle_participant_leave(self):
        room = TestRoom.objects.get(room_key=self.room_key)
        TestParticipant.objects.filter(user_id=self.user.id, room=room).delete()

        return self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'participant_update',
                'participants': list(room.participants.values_list('user__email', flat=True))
            }
        )

    async def participant_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'participant_update',
            'participants': event['participants']
        }))

    @database_sync_to_async
    def mark_participant_ready(self):
        room = TestRoom.objects.get(room_key=self.room_key)
        participant = TestParticipant.objects.get(user=self.user, room=room)
        participant.status = 'ready'
        participant.save()

        all_participants = room.participants.all()
        if all(p.status == 'ready' for p in all_participants):
            room.is_active = False
            room.save()

            return self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'test_ready'}
            )
    
    async def test_ready(self, event):
        await self.send(text_data=json.dumps({
            'type': 'test_ready'
        }))

    @database_sync_to_async
    def start_exam(self):
        room = TestRoom.objects.get(room_key=self.room_key)
        if not room.test:
            raise ValueError("No tests associated with this room")
        
        questions = list(room.test.questions.values('id', 'question_text'))
        return self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'exam_started',
                'questions': questions
            }
        )
    
    async def exam_started(self, event):
        await self.send(text_data=json.dumps({
            'type': 'exam_started',
            'questions': event['questions']
        }))

    @database_sync_to_async
    def handle_answer_submission(self, data):
        room = TestRoom.objects.get(room_key=self.room_key)
        question_id = data.get('question_id')
        answer_text = data.get('answer')

        if not question_id or not answer_text:
            raise ValueError("Invalid answer submission")
        
        question = Question.objects.get(id=question_id, test=room.test)
        participant = TestParticipant.objects.get(user=self.user, room=room)

        