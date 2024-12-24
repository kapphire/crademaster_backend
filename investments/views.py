from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from .models import Investment
# from .serializers import InvestmentSerializer

# class InvestmentListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Investment.objects.all()
#     serializer_class = InvestmentSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
    
#     def get_queryset(self):
#         """
#         Optionally filter the investments based on the logged-in user.
#         """
#         user = self.request.user
#         return Investment.objects.filter(user=user)
