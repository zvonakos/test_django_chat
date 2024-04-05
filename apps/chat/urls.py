from rest_framework import routers
from apps.chat.views import ThreadViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'threads', ThreadViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = router.urls
