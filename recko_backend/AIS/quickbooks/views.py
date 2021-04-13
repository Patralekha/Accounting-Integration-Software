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

from .serializers import EmptySerializer, QuickBooksSerializer,QuickBooksSerializer1,QNestedSerializer1,QNestedSerializer2,QNestedSerializer3,QNestedSerializer4

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.template import Context, loader

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

from .quickbooks_helper import constructUrl,quickbooksDataEntry


from services.models import Accounts



# Create your views here.
from django.contrib.auth import get_user_model,logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from . import serializers
from users.utils import get_and_authenticate_user,create_user_account
from users.models import CustomUser
from datetime import date


User = get_user_model()

############################     QUICKBOOKS CREDENTIALS     ############################

client_id1 = "AB1CT9l9mtRkuGnS9w9hASGJtnHTL0JhDggPIPM3gJy2W6gQAy"
client_secret1 = "GG6jhkVesyPyowXBYg9UVlGO1eJF3CUvEhXxfCiS"
redirect_uri1 = "http://localhost:8000/callback"
environment = "sandbox"
scopes = [
    Scopes.ACCOUNTING,
]
auth_client = AuthClient(client_id1, client_secret1, redirect_uri1,
                         environment)




#########################################################################################

#################################### QUICKBOOKS API CALL #########################################
def quickbook(request):
    url = auth_client.get_authorization_url(scopes)
    return redirect(url)


def callback(request):
    auth_code = request.GET.get('code', None)
    realm_id = request.GET.get('realmId', None)
    print("Auth code", " ", auth_code)
    print("Relam id", " ", realm_id)
    auth_client.get_bearer_token(auth_code, realm_id=realm_id)
    access_token = auth_client.access_token
    refresh_token = auth_client.refresh_token
    print(refresh_token)
    fetchUrl = reverse('qbo')
    return redirect(fetchUrl)


def fetchQboData(request):
    #map quickbooks data to serializer and store in database/update existing data in database
    #if auth_client.access_token is None:
    if auth_client.refresh_token is None:
        getNewTokenUrl = reverse('quickbook')
        return HttpResponseRedirect(getNewTokenUrl)
    else:
        auth_client.refresh()

    #call construct url function in quickbooks_helper.py
    #use for loop for pagination and sleep for timeouts and rate limit
    startposition=1
    maxresults=1000
    journalsFetched=0
    while True:
        response = constructUrl(auth_client.access_token, auth_client.realm_id,startposition,maxresults)
        r1=response.json()

        if response.status_code==429 or response.status_code==408:
            time.sleep(60)
            continue

        if not bool(r1['QueryResponse']):
            break
        else:
            journalsFetched += len(r1['QueryResponse']['JournalEntry'])

        rt_file = open('quickbooks_response.json', 'a')
        rt_file.write(response.text)
        rt_file.close()

        serializer=QuickBooksSerializer(data=r1)
        if serializer.is_valid():
            quickbooksDataEntry(r1)
        else:
            print(serializer.errors)
            template = loader.get_template("static/error.html")
            return HttpResponse(template.render())
        
        startposition=startposition+maxresults
        msg="You can close this window now and login again!!"
        template = loader.get_template("static/redirectQ.html")
    return HttpResponse(template.render())


                
##########################################################################################################################

############################     QUICKBOOKS FUNCTIONALITIES  ##################################


class QFunctionsViewSet(viewsets.GenericViewSet):
    ermission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'quickbooksAccounts':EmptySerializer,
        'quickbooksUsers':EmptySerializer,
    }

    queryset=''

    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def quickbooksAccounts(self, request):
        #returns quickbooks accounts page url
        adminPrivilege=User.objects.get(email=request.user.email).adminPrivilege
        if adminPrivilege:
            return Response(data={"url":"https://app.sandbox.qbo.intuit.com/app/chartofaccounts"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"You do not have administrator privilege!"},status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    
    def quickbooksUsers(self, request):
        #returns quickbooks users page url
        adminPrivilege=User.objects.get(email=request.user.email).adminPrivilege
        if adminPrivilege:
            return Response(data={"url":"https://app.sandbox.qbo.intuit.com/app/usermgt"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"You do not have administrator privilege"},status=status.HTTP_401_UNAUTHORIZED)


    
    