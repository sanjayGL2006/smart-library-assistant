from django.urls import path

from . import views

urlpatterns = [
    path(
        "chat/",
        views.ai_chat_page,
        name="knowledge-ai-chat"
    ),
    path(
        "api/ask/",
        views.ask_ai,
        name="knowledge-ai-ask"
    ),
]
