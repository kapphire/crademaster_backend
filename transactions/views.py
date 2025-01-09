from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import WithdrawSerializer

class WithdrawCreateAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
