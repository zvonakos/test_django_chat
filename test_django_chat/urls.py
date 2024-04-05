from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("chats/", include(
        ("apps.chat.urls", "apps.chat"), namespace='chats'
    )),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # I've decided to keep only this endpoint because it is prototype
]
