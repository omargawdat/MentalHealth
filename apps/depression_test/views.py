# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import TestQuestion

# # Using APIView class
# class TestAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({"message": "Hello from ds!"})
    
    
# class TestQuestionAPIView(APIView):
#     def get(self, request):
#         questions = TestQuestion.objects.all()
#         data = []
#         for question in questions:
#             options = question.answer_options.all().values('value', 'label')
#             data.append({
#                 'question': question.question,
#                 'answer_options': list(options)
#             })
#         return Response(data)
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TestQuestion, AnswerOption

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

    def post(self, request):
        answers = request.data.get('answers', [])
        total_score = 0

        for answer in answers:
            answer_value = answer.get('value')
            try:
                # Find the answer option with the matching value
                option = AnswerOption.objects.get(value=answer_value)
                total_score += option.value
            except AnswerOption.DoesNotExist:
                return Response({'error': 'Invalid answer value'}, status=status.HTTP_400_BAD_REQUEST)

        # Determine the level of depression based on the total_score
        level_of_depression = 'no depression'
        if 6 <= total_score <= 10:
            level_of_depression = 'normal but unhappy'
        elif 11 <= total_score <= 25:
            level_of_depression = 'mild depression'
        elif 26 <= total_score <= 50:
            level_of_depression = 'moderate depression'
        elif 51 <= total_score <= 75:
            level_of_depression = 'severe depression'
        elif 76 <= total_score <= 100:
            level_of_depression = 'extreme depression'

        return Response({'total_score': total_score, 'level_of_depression': level_of_depression})

class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello from ds!"})
    