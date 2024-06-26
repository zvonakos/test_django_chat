import uuid

from django.db import models
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

# I could've placed all these models Timestamp UUID and authentication as a separate app
# but in the given case I don't see it's quite necessary for now
# In case of a real project sure it requires purer differentiation


class TimeStamp(models.Model):
    """
    Represents a basic model which store information about time
    """
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True, editable=False, null=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True, editable=False, null=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Thread(TimeStamp, UUIDModel):
    participants = models.ManyToManyField(User, related_name='threads')

    def clean(self):  # Making sure that in thread were only 2 participants
        if self.participants.count() != 2:
            raise ValidationError('Only 2 user allowed')


class Message(TimeStamp, UUIDModel):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    is_read = models.BooleanField(default=False)
