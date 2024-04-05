from django.core.management.base import BaseCommand
from apps.chat.models import Thread, Message
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        users = User.objects.filter(pk__in=[1, 2, 3])

        for i, user1 in enumerate(users):
            for user2 in users[i + 1:]:
                thread = Thread.objects.create()
                thread.participants.add(user1, user2)

                for j in range(1, 6):
                    if j % 2 == 0:
                        sender = user2
                    else:
                        sender = user1
                    Message.objects.create(
                        thread=thread,
                        sender=sender,

                        text=f'Message {j} from user {sender.id} to user',
                        is_read=False
                    )