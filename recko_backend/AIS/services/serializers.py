
from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from .models import Accounts


class EmptySerializer(serializers.ModelSerializer):
    pass

######################################## TO SERIALIZE DATA FROM THE DATABASE #############################################

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Accounts
        fields=('accountId','accountName','amount','date','accountType','providerName','extraFields')
    


#################################### QUICKBOOKS JOURNALS SERIALIZER #######################################################

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
    Line=QNestedSerializer2(many=True)


class QuickBooksSerializer1(serializers.Serializer):
    JournalEntry=QNestedSerializer1(many=True)

class QuickBooksSerializer(serializers.Serializer):
    QueryResponse=QuickBooksSerializer1()
    time=serializers.DateTimeField()
    

###########################################  XERO JOURNAL SERIALIZER  #######################################################
    
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



    

