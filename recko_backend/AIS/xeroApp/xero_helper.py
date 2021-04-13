
import json
import requests
import webbrowser
import base64

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
import time
from datetime import datetime

from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

import requests
import json
from dateutil.parser import parse

from django.core.cache import cache

from .serializers import EmptySerializer, XeroSerializer, XNestedSerializer1, XNestedSerializer3,XNestedSerializer4

from services.models import Accounts
from django.core.management.base import BaseCommand

client_id = '53CA5E526A9C41AB91C216CC29C0A535'
client_secret = 'vh7Kar4K4FvGrbugjfzzEPCUvLD2t2b-p9SmLIR5cng30FgH'
redirect_url = 'http://localhost:8000/xero_callback'


scope = 'offline_access accounting.journals.read'
b64_id_secret = base64.b64encode(
    bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')


def XeroRefreshToken(refresh_token):
    token_refresh_url = 'https://identity.xero.com/connect/token'
    response = requests.post(token_refresh_url,
                             headers={
                                 'Authorization': 'Basic ' + b64_id_secret,
                                 'Content-Type': 'application/x-www-form-urlencoded'
                             },
                             data={
                                 'grant_type': 'refresh_token',
                                 'refresh_token': refresh_token
                             })
    json_response = response.json()
    print(json_response)

    new_refresh_token = json_response['refresh_token']
    cache.set('refresh_token',refresh_token,None)
    

    return [json_response['access_token'], json_response['refresh_token']]


def XeroTenants(access_token):
    connections_url = 'https://api.xero.com/connections'
    response = requests.get(connections_url,
                            headers={
                                'Authorization': 'Bearer ' + access_token,
                                'Content-Type': 'application/json'
                            })
    json_response = response.json()
    print(json_response)
    for tenants in json_response:
        json_dict = tenants
        return json_dict['tenantId']
    #print(json_dict)
    return json_dict['tenantId']


def constructXeroUrl(access_token, tid,offset):
    url = 'https://api.xero.com/api.xro/2.0/Journals?offset='+str(offset)
    response = requests.get(url,
                            headers={
                                'Authorization': 'Bearer ' + access_token,
                                'Xero-Tenant-Id': tid,
                                'Retry-After':"360000",
                                'Accept': 'application/json'
                            })
    print(response)
    return response


def xeroDataEntry(response):
    for obj in response['Journals']:
        list1 = []
        extra={}
        dt = datetime.fromtimestamp(int(obj['JournalDate'][6:-10]))
        extra['JournalNumber']=obj['JournalNumber']
        date = dt.strftime('%Y-%m-%d')
        for journalLine in obj['JournalLines']:
            s1 = XNestedSerializer3(data=journalLine)
            if s1.is_valid():
                accountId = s1.data.get('AccountCode')
                accountName = s1.data.get('AccountName')
                amount = s1.data.get('GrossAmount')
                accType = 'Debit'

                net = s1.data.get('NetAmount')
                if net < 0:
                    accType = "Credit"
                else:
                    accType = "Debit"


                extra['AccountID']=s1.data.get('AccountID')
                extra['AccountType']=s1.data.get('AccountType')
                extra['TaxAmount']=s1.data.get('TaxAmount')
                
                extraField=json.dumps(extra,indent=4)
                print(extra,"\n")
                if Accounts.objects.filter(accountName=accountName, accountId=accountId, amount=amount, date=date, accountType=accType, providerName="Xero").exists() is False:
                    record = Accounts(accountName=accountName, accountId=accountId,
                                      amount=amount, date=date, accountType=accType, providerName="Xero",extraFields=extraField)
                    record.save()
                else:
                    record=Accounts.objects.filter(accountName=accountName, accountId=accountId, amount=amount, date=date, accountType=accType, providerName="Xero")[0]
                    record.extraFields=extraField
                    record.save()

                list1.append(s1.data)
            else:
                print(s1.errors)
