from django.contrib import admin

from apps.chat.models import Thread, Message


admin.site.register(Thread)
admin.site.register(Message)