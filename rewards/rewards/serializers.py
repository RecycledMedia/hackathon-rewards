from rest_framework import serializers
from rewards.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user_id', 'summary', 'description', 'points', 'timestamp']