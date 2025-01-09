from rest_framework import serializers
from .models import Withdraw

class WithdrawSerializer(serializers.ModelSerializer):

    class Meta:
        model = Withdraw
        fields = ['id', 'user', 'amount', 'address', 'status', 'requested_at', 'completed_at']
        read_only_fields = ['id', 'user', 'status', 'requested_at', 'completed_at']

    def validate(self, data):
        """
        Validate that the user can create a Usage record only once per day.
        """
        user = self.context['request'].user
        if Withdraw.objects.filter(user=user, status='PENDING').exists():
            raise serializers.ValidationError("You already have a pending withdrawal request.")
        
        if data['amount'] > user.get_usdt_balance:
            raise serializers.ValidationError("Exceed amount.")
        return data
