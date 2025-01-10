from django.utils.timezone import now
from rest_framework import serializers

from fees.models import Fee
from .models import Execute


class ExecuteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Execute
        fields = ['id', 'user', 'amount', 'duration', 'created']
        read_only_fields = ['id', 'user', 'amount', 'duration', 'created']

    def validate(self, data):
        """
        Validate that the user can create a Execute record only once per day.
        """
        user = self.context['request'].user
        today = now().date()

        if user.get_usdt_balance == 0:
            raise serializers.ValidationError("Your USDT balance is zero. Please deposit funds to proceed.")

        if Execute.objects.filter(user=user, created__date=today).exists():
            raise serializers.ValidationError("You can only activate the platform once per day.")

        return data

    def create(self, validated_data):
        user = validated_data.get('user')
        amount = user.get_usdt_balance

        applicable_fee = Fee.objects.filter(min_investment__lte=amount, max_investment__gte=amount).first()

        if not applicable_fee:
            raise serializers.ValidationError("No fee found for the given investment amount.")

        usage = Execute.objects.create(duration=applicable_fee.hours, user=user, amount=amount, profit_percent=user.profit_percent)
        return usage
