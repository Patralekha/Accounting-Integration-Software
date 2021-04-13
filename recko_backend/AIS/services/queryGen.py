from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import EmptySerializer, DataSerializer, XeroSerializer, XNestedSerializer1, QuickBooksSerializer, QuickBooksSerializer1, XNestedSerializer3, QNestedSerializer1, QNestedSerializer2, QNestedSerializer3, QNestedSerializer4

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


from .models import Accounts


# Create your views here.
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers
from users.utils import get_and_authenticate_user, create_user_account
from users.models import CustomUser
from datetime import date


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from functools import reduce
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
from operator import and_

from decimal import Decimal
import datetime

User = get_user_model()

dateformat='%Y-%m-%d'

def queryset_generator(accName,openAmt,closeAmt,stDate,endDate,de,cr,st,ed):
    #no filters set
    queryset=Accounts.objects.values('accountId','accountName','amount','date','accountType','providerName')
    if not accName and not openAmt and not closeAmt and not stDate and not endDate and not de and not cr:
        print("No filter set")
        queryset=Accounts.objects.values('accountId','accountName','amount','date','accountType','providerName','extraFields').order_by('-date')[st:ed]

    if accName:
        print("filter acc set")
        queryset=queryset.filter(accountName=accName)
    
    if openAmt and closeAmt:
        print("filter amt both set")
        queryset=queryset.filter(amount__range=[Decimal(openAmt),Decimal(closeAmt)])
    elif not openAmt and closeAmt:
        print("filter amt close set")
        queryset=queryset.filter(amount__lte=Decimal(closeAmt))
    elif openAmt and not closeAmt:
        print("filter amt open set")
        queryset=queryset.filter(amount__gte=Decimal(openAmt))

    
    if de and not cr:
        print("filter de  set")
        queryset=queryset.filter(accountType=de)
    elif not de and cr:
        print("filter cr  set")
        queryset=queryset.filter(accountType=cr)


    if stDate and endDate:
        print("filter sd and ed  set")
        s=datetime.datetime.strptime(stDate, dateformat).date()
        e=datetime.datetime.strptime(endDate, dateformat).date()
        queryset=queryset.filter(date__range=[stDate, endDate])
    elif not stDate and endDate:
        print("filter ed  set")
        e=datetime.datetime.strptime(endDate, dateformat).date()
        queryset=queryset.filter(date__lte=endDate)
    elif stDate and not endDate:
        print("filter sd set")
        s=datetime.datetime.strptime(stDate, dateformat).date()
        queryset=queryset.filter(date__gte=stDate)

    return queryset

        