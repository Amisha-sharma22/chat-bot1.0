from django.urls import path
from .views import chat_api, home

urlpatterns = [
    path('', home, name='home'),  # Add this line
    path('api/chat/', chat_api, name='chat_api'),
    # other paths
]
