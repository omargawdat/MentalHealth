from rest_framework.response import Response
from rest_framework.views import APIView


# Using APIView class
class TestAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello from TestAPIView!"})
