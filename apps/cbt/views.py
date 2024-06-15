from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import NegativeThinkingType, CBTQuestion
from .serializer import NegativeThinkingTypeSerializer, CBTQuestionSerializer


class NegativeThinkingTypeList(generics.ListAPIView):
    queryset = NegativeThinkingType.objects.all()
    serializer_class = NegativeThinkingTypeSerializer
    permission_classes = []


class CBTQuestionListByType(APIView):
    def post(self, request, *args, **kwargs):
        type_ids = request.data.get('type_ids', [])
        questions = CBTQuestion.objects.filter(models.Q(thinking_type__in=type_ids) | models.Q(is_general=True))
        serializer = CBTQuestionSerializer(questions, many=True)
        return Response(serializer.data)
