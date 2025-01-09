from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class ReferredUserSerializer(serializers.ModelSerializer):
    earning = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'created', 'earning']

    def get_earning(self, obj):
        return 0
