from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rewards.models import Transaction
from rewards.serializers import TransactionSerializer

