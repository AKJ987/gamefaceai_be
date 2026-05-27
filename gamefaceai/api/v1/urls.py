from api.v1 import views
from django.urls import path

urlpatterns = [
    path("game/face/ai/", views.GameFaceAIAPIView.as_view(), name="game-face-ai"),
]
