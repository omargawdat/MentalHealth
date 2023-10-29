from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TestQuestion

# Using APIView class
class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello from ds!"})
    
    
class TestQuestionAPIView(APIView):
    def get(self, request):
        questions = TestQuestion.objects.all()
        data = []
        for question in questions:
            options = question.answer_options.all().values('value', 'label')
            data.append({
                'question': question.question,
                'answer_options': list(options)
            })
        return Response(data)
    
    
