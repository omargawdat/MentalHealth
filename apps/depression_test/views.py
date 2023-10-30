from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import DepressionLevel
from .models import AnswerOption, DepressionAssessment, TestQuestion
from .serializers import AnswerOptionSerializer, SumNumbersSerializer, TestQuestionSerializer


class CalculateTestView(APIView):

    def post(self, request):
        serializer = SumNumbersSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        scores = serializer.validated_data['answers']
        total_score = sum(scores)
        level_of_depression = DepressionLevel.NO_DEPRESSION
        if 6 <= total_score <= 10:
            level_of_depression = DepressionLevel.NORMAL_BUT_UNHAPPY
        elif 11 <= total_score <= 25:
            level_of_depression = DepressionLevel.MILD_DEPRESSION
        elif 26 <= total_score <= 50:
            level_of_depression = DepressionLevel.MODERATE_DEPRESSION
        elif 51 <= total_score <= 75:
            level_of_depression = DepressionLevel.SEVERE_DEPRESSION
        elif 76 <= total_score <= 100:
            level_of_depression = DepressionLevel.EXTREME_DEPRESSION

        DepressionAssessment.objects.create(
            user=request.user,
            total_score=total_score,
            level_of_depression=level_of_depression.value
        )
        
        return Response({'total_score': total_score, 'level_of_depression': level_of_depression.value})


class TestQuestionListView(ListAPIView):
    queryset = TestQuestion.objects.all()
    serializer_class = TestQuestionSerializer
    permission_classes = []


class AnswerOptionListView(ListAPIView):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializer
    permission_classes = []
