from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.chat.models import Thread, Message
from apps.chat.serializers import ThreadSerializer, MessageSerializer


class CustomMessagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ThreadSerializer
    pagination_class = CustomMessagePagination

    def create(self, request, *args, **kwargs):

        data = self.request.data

        # wish I could make the check if the thread exists more aesthetic but couldn't figure it out
        existing_thread = Thread.objects.filter(
            participants__id=data.get('participants')[0]['id']
        ).filter(
            participants__id=data.get('participants')[1]['id']
        ).first()
        if existing_thread:
            return Response(data={
                'thread': existing_thread.id
            }, status=201)
        else:
            thread = Thread.objects.create()  # creating thread and adding messages to it
            thread.participants.add(data['participants'][0]['id'], data['participants'][1]['id'])
            thread.save()
            messages = data.pop('messages')
            messages = [
                Message(
                    thread=thread, sender=self.request.user, text=item['text'], is_read=item['is_read']
                ) for item in messages
            ]
            Message.objects.bulk_create(messages)
            return Response(data={
                'thread': thread.id  # There might be a necessity to return more data from a more accurate integration with frontend but i've left only thread id
            }, status=201)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()

        if pk:
            messages = Message.objects.filter(thread=pk)
            messages.exclude(sender=request.user).update(is_read=True)  # here marking the messages as read

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request, *args, **kwargs):
        user = request.user
        unread_messages_count = Message.objects.exclude(sender=user).filter(is_read=False) \
            .values('sender') \
            .annotate(unread_count=Count('id'))  # making a count of unread messages via ORM
        return Response([
            {
                'user_id': unread['sender'],
                'number_of_messages': unread['unread_count']
            } for unread in
            unread_messages_count
        ])


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data
        message = Message.objects.create(
            thread=Thread.objects.get(id=data['thread']),
            sender=self.request.user,
            text=data['text'],
            is_read=data['is_read']
        )
        return Response(data={
            'message': message.id  # I realise there might be a necessity to return more data from a more accurate integration with frontend but i've left only message id
        }, status=201)
