from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import *
from datetime import datetime, timedelta
from rest_framework.parsers import JSONParser
from rewards.models import *
from rewards.serializers import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status



@csrf_exempt
def transaction_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Transaction.objects.all()
        serializer = TransactionSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def tiers(request):
    if request.method == 'GET':
        tiers = Tier.objects.all()
        serializer = TierSerializer(tiers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TierSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def tierDetail(request, tier_id):
    if request.method == 'GET':
        tier = Tier.objects.get(id=tier_id)
        serializer = TierSerializer(tier, many=False)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'DELETE':
        try:
          tier = Tier.objects.get(id=tier_id)
          tier.delete()
          return JsonResponse('', status=status.HTTP_204_NO_CONTENT, safe=False)
        except ObjectDoesNotExist as e:
          return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        payload = json.loads(request.body)
        try:
            tier_item = Tier.objects.filter(id=tier_id)
            # returns 1 or 0
            tier_item.update(**payload)
            tier = Tier.objects.get(id=tier_id)
            serializer = TierSerializer(tier, many=False)
            return JsonResponse({serializer.data}, safe=False, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#@api_view(["GET"])
@csrf_exempt
def getUserBalance(request, user_id):
    balance = Transaction.objects.filter(user_id=user_id, ).aggregate(Sum('points'))["points__sum"]
    return JsonResponse({"user_id": user_id, "balance": str(balance)}, safe=False, status=status.HTTP_200_OK)
#    tier_balance =
#    tier_num =  Tier.objects.filter(user_id__gt=balance).aggregate(Max())


def getTierPoints(request, user_id):
    tierBalance = Transaction.objects.filter(
        user_id=user_id,
        points__gte=0,
        timestamp__gte=datetime.now()-timedelta(days=365)
        ).aggregate(Sum('points'))["points__sum"]
    return JsonResponse({"user_id": user_id, "tierPoints": str(tierBalance)}, safe=False, status=status.HTTP_200_OK)


def getTier(request, user_id):
    tierBalance = Transaction.objects.filter(
        user_id=user_id,
        points__gte=0,
        timestamp__gte=datetime.now()-timedelta(days=365)
        ).aggregate(Sum('points'))["points__sum"]
    tier = Tier.objects.filter(
        threshold__lte = tierBalance
    ).order_by('-rank')[0]
    serializer = TierSerializer(tier, many=False)
    return JsonResponse(serializer.data, safe=False)

def getUserDetails(request, user_id):
    balance = Transaction.objects.filter(user_id=user_id, ).aggregate(Sum('points'))["points__sum"]
    tierBalance = Transaction.objects.filter(
        user_id=user_id,
        points__gte=0,
        timestamp__gte=datetime.now()-timedelta(days=365)
        ).aggregate(Sum('points'))["points__sum"]
    tier = Tier.objects.filter(
        threshold__lte = tierBalance
    ).order_by('-rank')[0]
    return JsonResponse({"user_id": str(user_id), "balance": str(balance), "tier_id": str(tier.id), "tier_summary": str(tier.summary), "tierPoints": str(tierBalance)}, safe=False, status=status.HTTP_200_OK)

#def getUserTier(request, user_id):
#    echo ""

# class UserInfo(APIView):

#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)
