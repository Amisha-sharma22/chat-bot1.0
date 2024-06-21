from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatSerializer
from .model import ChatbotModel
from django.http import HttpResponse

# Load the chatbot model once at startup
chatbot_model = ChatbotModel('D:/testing/DemoBot/Bot/test.txt', model_path='D:/testing/DemoBot/Bot/.model/chatbot_model.h5')

@api_view(['POST'])
def chat_api(request):
    if request.method == 'POST':
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            user_input = serializer.validated_data['user_input']
            response = chatbot_model.generate_text(user_input, next_words=20)
            return Response({'response': response}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return HttpResponse("Welcome to the Chatbot API! Go to /api/chat/ to interact with the chatbot.")
