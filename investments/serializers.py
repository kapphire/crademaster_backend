from django.utils.timezone import now
from rest_framework import serializers
from .models import Investment, Fee, Usage

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


class UsageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usage
        fields = ['id', 'user', 'amount', 'duration', 'created']
        read_only_fields = ['id', 'user', 'amount', 'duration', 'created']

    def validate(self, attrs):
        """
        Validate that the user can create a Usage record only once per day.
        """
        user = self.context['request'].user
        today = now().date()

        if Usage.objects.filter(user=user, created__date=today).exists():
            raise serializers.ValidationError("You can only activate the platform once per day.")

        return attrs

    def create(self, validated_data):
        user = validated_data.get('user')
        amount = user.get_usdt_balance

        applicable_fee = Fee.objects.filter(min_investment__lte=amount, max_investment__gte=amount).first()

        if not applicable_fee:
            raise serializers.ValidationError("No fee found for the given investment amount.")

        usage = Usage.objects.create(duration=applicable_fee.hours, user=user, amount=amount)
        return usage
