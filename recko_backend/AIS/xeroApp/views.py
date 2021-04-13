################################################################################
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import EmptySerializer, XeroSerializer, XNestedSerializer1, XNestedSerializer3,XNestedSerializer4

from django.core.cache import cache

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect

from intuitlib.client import AuthClient
from intuitlib.enums import Scopes
from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes

import requests
import json
import datetime
import base64
import schedule
import time


from .xero_helper import constructXeroUrl, XeroRefreshToken, XeroTenants, xeroDataEntry

from services.models import Accounts


# Create your views here.
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.template import Context, loader

from . import serializers
from users.utils import get_and_authenticate_user, create_user_account
from users.models import CustomUser
from datetime import date


User = get_user_model()


############################      XERO CREDENTIALS    ###################################

client_id = '53CA5E526A9C41AB91C216CC29C0A535'
client_secret = 'vh7Kar4K4FvGrbugjfzzEPCUvLD2t2b-p9SmLIR5cng30FgH'
redirect_url = 'http://localhost:8000/xero_callback'

scope = 'offline_access accounting.journals.read'
b64_id_secret = base64.b64encode(
    bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')


#########################################################################################


########################################  XERO API CALL #################################

def xero(request):
    auth_url = ('''https://login.xero.com/identity/connect/authorize?''' +
                '''response_type=code''' + '''&client_id=''' + client_id +
                '''&redirect_uri=''' + redirect_url + '''&scope=''' + scope +
                '''&state=123''')
    return redirect(auth_url)


def xero_callback(request):
    auth_code = request.GET.get('code', None)
    print(auth_code)

    exchange_code_url = 'https://identity.xero.com/connect/token'
    response = requests.post(
        exchange_code_url,
        headers={'Authorization': 'Basic ' + b64_id_secret},
        data={
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_url
        })

    json_response = response.json()
    print(json_response)

    refresh_token = json_response['refresh_token']

    
    if cache.has_key('refresh_token'):
       cache.delete('refresh_token')
    cache.set('refresh_token',refresh_token)

    access_token = json_response['access_token']
    print(refresh_token)

    
    cache.set('access_token',access_token)
    template = loader.get_template("static/redirectX.html")
    return HttpResponse(template.render())

def fetchXeroData(request):
    old_refresh_token =cache.get('refresh_token') #open('refresh_token.txt', 'r').read() 


    print(old_refresh_token)
    new_tokens = XeroRefreshToken(old_refresh_token)
    xero_tenant_id = XeroTenants(new_tokens[0])
   

    
    # use for loop and record offset number,increment offset number by 100
    offset = 0
    journalsFetched = 0
    while True: 
        response = constructXeroUrl(new_tokens[0], xero_tenant_id, offset)
        r = response.json()
        print(r)

        if response.status_code==429 or response.status_code==408:
            time.sleep(response.headers['Retry-After'])
            continue

        if len(r['Journals']) == 0:
            break
        else:
            journalsFetched += len(r['Journals'])

        serializer = XeroSerializer(data=r)
        if serializer.is_valid():
            #print(serializer.data)
            xeroDataEntry(r)
        else:
            print(serializer.errors)
            template = loader.get_template("static/error.html")
            return HttpResponse(template.render())
        
        offset += 100
    msg="You can close this window now and login again!!"
    template = loader.get_template("static/redirectX.html")
    return HttpResponse(template.render())

    




class XFunctionsViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'xeroAccounts':EmptySerializer,
        'xeroUsers':EmptySerializer
    }

    queryset=''


    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def xeroAccounts(self, request):
        #returns xero accounts page url
        adminPrivilege=User.objects.get(email=request.user.email).adminPrivilege
        if adminPrivilege:
            return Response(data={"url":"https://go.xero.com/GeneralLedger/ChartOfAccounts.aspx"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"You do not have administrator privilege!!"},status=status.HTTP_401_UNAUTHORIZED)
        
    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def xeroUsers(self, request):
        #returns xero users page url
        adminPrivilege=User.objects.get(email=request.user.email).adminPrivilege
        if adminPrivilege:
            return Response(data={"url":"https://go.xero.com/Settings/Users"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"You do not have administrator privilege"},status=status.HTTP_401_UNAUTHORIZED)