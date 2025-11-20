from rest_framework import serializers
from loan.models import Repayment

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = ['id', 'loan', 'amount', 'timestamp']
        read_only_fields = ['id', 'timestamp']  # timestamp will be set automatically

    def create(self, validated_data):
        # Set timestamp automatically
        from django.utils import timezone
        validated_data['timestamp'] = timezone.now()
        return super().create(validated_data)