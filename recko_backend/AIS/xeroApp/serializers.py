
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from services.models import Accounts


class EmptySerializer(serializers.ModelSerializer):
    pass

###########################################  XERO JOURNAL SERIALIZER  #######################################################
class XNestedSerializer4(serializers.Serializer):
    Name=serializers.CharField()
    Option=serializers.CharField()
    TrackingCategoryID=serializers.CharField()
    TrackingOptionID=serializers.CharField()


class XNestedSerializer3(serializers.Serializer):  
    TaxType=serializers.SerializerMethodField()
    TaxName=serializers.SerializerMethodField()
    JournalLineID=serializers.CharField()
    AccountID=serializers.CharField()
    AccountCode=serializers.CharField()
    AccountType=serializers.CharField()
    AccountName=serializers.CharField()
    NetAmount=serializers.FloatField()
    GrossAmount=serializers.FloatField()
    TaxAmount=serializers.FloatField()
    
    

    def get_TaxName(self,obj):
        if hasattr(obj,'TaxName'):
            print('TaxName')
            return obj.TaxName
        else:
            return "Null"

    def get_TaxType(self,obj):
        if hasattr(obj,'TaxType'):
            return obj.TaxType
        else:
            return "Null"
   

    


class XNestedSerializer1(serializers.Serializer):
    JournalID=serializers.CharField()
    JournalDate=serializers.CharField()
    JournalNumber=serializers.IntegerField()
    CreatedDateUTC=serializers.CharField()
    JournalLines=XNestedSerializer3(many=True)



class XeroSerializer(serializers.Serializer):
    Id=serializers.CharField()
    ProviderName=serializers.CharField()
    Journals=XNestedSerializer1(many=True)