from django.urls import path

from . import views

urlpatterns = [
    path(
        "api/ask/",
        views.ask_ai,
        name="knowledge-ai-ask"
    ),
]
