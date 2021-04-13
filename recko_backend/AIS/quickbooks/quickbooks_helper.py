import json
import requests
import webbrowser
import base64

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
import datetime
from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
import requests
import json
# Create your views here.
from django.core.cache import cache
from .serializers import EmptySerializer, QuickBooksSerializer,QuickBooksSerializer1,QNestedSerializer1,QNestedSerializer2,QNestedSerializer3,QNestedSerializer4

from services.models import Accounts
from django.core.management.base import BaseCommand


def constructUrl(token,realm_id,startposition,maxresults):
    base_url = 'https://sandbox-quickbooks.api.intuit.com'

    url = '{0}/v3/company/{1}/query?query=select * from journalentry startposition {2} maxresults {3} & minoversion=57'.format(
        base_url, realm_id,startposition,maxresults)
    auth_header = 'Bearer {0}'.format(token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    #change this to fetch all journals
    payload = "select * from journalentry startposition 1 maxresults 5"
    
    response = requests.request('GET',url, headers=headers)
    return response 
    


def quickbooksDataEntry(response):
    for obj in response['QueryResponse']['JournalEntry']:
        list1 = []
        extra={}
        date=obj['TxnDate']
        extra['JournalID']=obj['Id']
        extra['CurrencyRef']=obj['CurrencyRef']
        for journalLine in obj['Line']:
                s1 = QNestedSerializer2(data=journalLine)
                if s1.is_valid():
                    accountId=journalLine['JournalEntryLineDetail']['AccountRef']['value']
                    accountName=journalLine['JournalEntryLineDetail']['AccountRef']['name']
                    accountType=journalLine['JournalEntryLineDetail']['PostingType']
                    amount=s1.data.get('Amount')
                    extra['Description']=s1.data.get('Description')
                    extra['DetailType']=s1.data.get('DetailType')
                    print("Date: ",date)
                    print("Account Id: ",accountId,"\n")
                    print("Account Name: ",accountName,"\n")
                    print("Account Type: ",accountType,"\n")
                    print("Amount: ",amount,"\n")
                    print("Extra Fields",extra)
                    extraField=json.dumps(extra, indent = 4)
                    if Accounts.objects.filter(accountName=accountName, accountId=accountId,amount=amount,date=date,accountType=accountType,providerName="Quickbooks").exists() is False:
                        record=Accounts(accountName=accountName, accountId=accountId,amount=amount,date=date,accountType=accountType,providerName="Quickbooks",extraFields=extraField)
                        record.save()
                    else:
                        record=Accounts.objects.filter(accountName=accountName, accountId=accountId,amount=amount,date=date,accountType=accountType,providerName="Quickbooks")[0]
                        record.extraFields=extraField
                        record.save()
                else:
                    print(s1.errors)