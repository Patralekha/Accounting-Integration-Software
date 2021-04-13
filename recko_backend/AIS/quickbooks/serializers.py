
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from services.models import Accounts


class EmptySerializer(serializers.ModelSerializer):
    pass



class QNestedSerializer4(serializers.Serializer):
    name=serializers.CharField()
    value=serializers.IntegerField()



class QNestedSerializer3(serializers.Serializer):
    PostingType=serializers.CharField()
    AccountRef=QNestedSerializer4()


class QNestedSerializer2(serializers.Serializer):
    JournalEntryLineDetail=QNestedSerializer3()
    DetailType=serializers.CharField()
    Amount=serializers.FloatField()
    Id=serializers.IntegerField()
    Description=serializers.CharField()


class QNestedSerializer1(serializers.Serializer):
    Adjustment=serializers.BooleanField()
    domain=serializers.CharField()
    Id=serializers.IntegerField()
    SyncToken=serializers.IntegerField()
    TxnDate=serializers.DateField()
    sparse=serializers.BooleanField()
    CurrencyRef=serializers.JSONField()
    Line=QNestedSerializer2(many=True)


class QuickBooksSerializer1(serializers.Serializer):
    JournalEntry=QNestedSerializer1(many=True)

class QuickBooksSerializer(serializers.Serializer):
    QueryResponse=QuickBooksSerializer1()
    time=serializers.DateTimeField()
    