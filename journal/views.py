from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import jornalentry
from apps.authentication.models import CustomUser
from .serializers import JournalSerializer
from rest_framework import generics

# Using APIView class
# class TestAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({"message": "Hello from journal!"})

class JournalEntryListCreateView(generics.ListCreateAPIView):
    queryset = jornalentry.objects.all()
    serializer_class = JournalSerializer

class JournalEntryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = jornalentry.objects.all()
    serializer_class = JournalSerializer
    
@api_view(['GET'])
def get_journal_entries_by_user_id(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    entries = jornalentry.objects.filter(user=user)
    serializer = JournalSerializer(entries, many=True)  # Create a serializer for the entries
    return Response(serializer.data)
