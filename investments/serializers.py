from rest_framework import serializers
from .models import Investment, Fee

class InvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ['user', 'amount', 'fee', 'created']

    def validate_amount(self, value):
        """
        Ensure that the amount is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError("Investment amount must be positive.")
        return value

    def create(self, validated_data):
        amount = validated_data['amount']
        user = validated_data.get('user')

        # Find the fee that applies based on the amount
        applicable_fee = Fee.objects.filter(min_investment__lte=amount, max_investment__gte=amount).first()

        if not applicable_fee:
            raise serializers.ValidationError("No fee found for the given investment amount.")

        investment = Investment.objects.create(fee=applicable_fee, user=user, **validated_data)
        return investment
