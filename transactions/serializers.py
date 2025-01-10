from rest_framework import serializers
from .models import Transaction

class WithdrawSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'address', 'status', 'requested_at', 'completed_at']
        read_only_fields = ['id', 'user', 'status', 'requested_at', 'completed_at']

    def validate(self, data):
        user = self.context['request'].user
        if Transaction.objects.filter(user=user, status='PENDING').exists():
            raise serializers.ValidationError("You already have a pending withdrawal request.")
        
        if data['amount'] > user.get_usdt_balance:
            raise serializers.ValidationError("Exceed amount.")
        return data
