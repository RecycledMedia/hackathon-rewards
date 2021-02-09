from django.db import models


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(null=False)
    summary = models.CharField(
        max_length=255,
        null=False,
    )
    description = models.CharField(
        max_length=255,
        null=False,
    )
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Tier(models.Model):
    id = models.IntegerField(primary_key=True)
    summary = models.CharField(
        max_length=255,
        null=False,
    )
    description = models.CharField(
        max_length=255,
        null=False,
    )
    # number of points required to hit tier (yearly)
    threshold  = models.IntegerField()
    rank = models.IntegerField()

# Models
# Transaction
# - user_id
# - Summary
# - Description
# - Points
# - dateTime
# - UUID
# Reward
# - id
# - Summary
# - Description
# - Points
# Tier
# - id
# - Summary
# - Description
# - Threshold
# - Tier number (higher = more valuable)
#
# Action
# - id
# - Summary
# - Description
# - Weight (ability to assign different numbers of points to different events)
#
# Endpoints:
# /transaction/ - list transactions
# /reward/ - CRUD
# /actions/ - CRUD
# /actions/execute - creates transaction for earned actions (money spent, like, etc) - post data contains UUID, responds with sequential id + UUID
# /reward/redeem - post user + reward ID - add coupon to account - create transaction entry
# /tier - CRUD tier
#
# Not sure we need to store any data about the user but nice to get stats:
# /user/:user_id/tierPoints - returns points earned by user in the past 365 days (inclusive)
# /user/:user_id/tier - gets current tier for supplied user (gets
# /user/:user_id/balance - calculates points balance
