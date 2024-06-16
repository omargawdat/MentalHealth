from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnswerOption, TestQuestion
from .models import DepressionTestAttempt
from .serializer import DepressionTestAttemptSerializer


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
        description = 'No signs of depression. Continue maintaining a healthy lifestyle.'
        if 6 <= total_score <= 10:
            level_of_depression = 'normal but unhappy'
            description = (
                'You may be experiencing normal levels of unhappiness. This might be '
                'due to recent life events or stress. It is recommended to monitor '
                'your feelings and seek support if needed.'
            )
        elif 11 <= total_score <= 25:
            level_of_depression = 'mild depression'
            description = (
                'Mild depression is characterized by persistent sadness or low mood '
                'that may affect daily activities. Self-help strategies, such as '
                'regular exercise, maintaining social connections, and practicing '
                'mindfulness, can be beneficial. Professional support might be '
                'considered if symptoms persist.'
            )
        elif 26 <= total_score <= 50:
            level_of_depression = 'moderate depression'
            description = (
                'Moderate depression includes more significant symptoms that impact '
                'daily functioning. It is advisable to seek professional support, '
                'such as therapy or counseling. Cognitive Behavioral Therapy (CBT) '
                'and other therapeutic approaches can be effective in managing symptoms.'
            )
        elif 51 <= total_score <= 75:
            level_of_depression = 'severe depression'
            description = (
                'Severe depression greatly affects daily life and requires immediate '
                'attention. Professional treatment, including therapy and possibly '
                'medication, is strongly recommended. A comprehensive treatment plan '
                'tailored to individual needs can significantly improve well-being.'
            )
        elif 76 <= total_score <= 100:
            level_of_depression = 'extreme depression'
            description = (
                'Extreme depression is a critical condition that requires urgent '
                'medical intervention. Immediate professional help is essential. '
                'Hospitalization or intensive outpatient programs may be necessary '
                'to ensure safety and provide intensive treatment.'
            )

        test_attempt = DepressionTestAttempt(
            user=request.user,
            total_score=total_score,
            level_of_depression=level_of_depression,
            timestamp=now()
        )
        test_attempt.save()

        response_data = {
            'total_score': total_score,
            'level_of_depression': level_of_depression,
            'description': description
        }

        return Response(response_data, status=status.HTTP_200_OK)


class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello from ds!"})


class DepressionTestHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        test_attempts = DepressionTestAttempt.objects.filter(user=user).order_by('-timestamp')
        serializer = DepressionTestAttemptSerializer(test_attempts, many=True)
        return Response(serializer.data)
