from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ExecuteSerializer


class ExecuteCreateAPIView(generics.CreateAPIView):
    serializer_class = ExecuteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
