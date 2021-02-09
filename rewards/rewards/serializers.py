from rest_framework import serializers
from rewards.models import *

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user_id', 'summary', 'description', 'points', 'timestamp']

class TierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
         model = Tier
         fields = ['id', 'summary', 'description', 'threshold', 'rank']
