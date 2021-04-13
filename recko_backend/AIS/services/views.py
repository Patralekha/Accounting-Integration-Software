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


from .queryGen import queryset_generator


User = get_user_model()


class TransactionViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'transactions': EmptySerializer,
        'getTotalRecs':EmptySerializer,
        'transactionsPaginated': EmptySerializer,
        'filterByDate': EmptySerializer,
        'filterByType': EmptySerializer,
        'filterByAccName': EmptySerializer,
        'xeroAccounts': EmptySerializer,
        'xeroUsers': EmptySerializer
    }

    queryset = ''

    @action(methods=['GET','POST'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def transactions(self, request):
        #returns data from our database
        accName=request.data['accName']
        openAmt=request.data['stAmt']
        closeAmt=request.data['endAmt']
        stDate=request.data['stDate']
        endDate=request.data['endDate']
        de=request.data['de']
        cr=request.data['cr']
        start=int(request.data['start']) if request.data['start'] != '' else 0
        end=int(request.data['end']) if request.data['end'] != '' else 0
        print(start," ",end)
        queryset=queryset_generator(accName,openAmt,closeAmt,stDate,endDate,de,cr,start,end)
        print(len(queryset))
        serializer=DataSerializer(queryset,many=True)
        return Response(serializer.data,status.HTTP_200_OK)


    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def getTotalRecs(self, request):
        #returns data from our database
        num=Accounts.objects.all().count()
        print(num)
        num1=Accounts.objects.count()
        print(num1)
        sets=1
        total=num1
        num2=num1
        if num1%1000==num1:
            sets=1
        else:
            cnt=divmod(num1, 1000)           
            sets=cnt[0] if cnt[1]==0 else cnt[0]+1
        return Response(data={"sets":sets,"totalRecords":total,"lastSet":cnt[1]},status=status.HTTP_200_OK)




    @action(methods=['GET'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def transactionsPaginated(self, request):
        print(request.data)
        fields=['accountId','accountName','amount','accountType','date']
        dt = (request.GET)
        draw = int(dt.get('draw'))
        start = int(dt.get('start'))
        length = int(dt.get('length'))
        search = dt.get('search[value]')
        colOrder=int(dt.get('order[0][column]'))
        field='accountId'
        if colOrder >=0:
            if dt.get('order[0][dir]') == 'asc':
                field=fields[colOrder]
            else:
                field="-"+fields[colOrder]

        print(field)
        records_total = Accounts.objects.all().exclude(Q(accountId=None) | Q(
            accountName=None) | Q(amount=None) | Q(accountType=None) | Q(date=None)).count()
        records_filtered = records_total
        accounts = Accounts.objects.all().order_by(field)
        if search:
            accounts = Accounts.objects.filter(
                    Q(accountId__icontains=search) |
                    Q(accountName__icontains=search) |
                    Q(amount__icontains=search) |
                    Q(accountType__icontains=search) |
                    Q(date__icontains=search)
                ).order_by(field)
            records_total = accounts.count()
            records_filtered = records_total

           
        paginator = Paginator(accounts, length)
        pg=start / length + 1

        try:
            object_list = paginator.page(pg).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages).object_list

        

        data = [
            {
                'accountId': inv.accountId,
                'accountName': inv.accountName,
                'amount': inv.amount,
                'accountType': inv.accountType,
                'date': inv.date,
            } for inv in object_list
        ]

        print(records_filtered," ",records_total," ",len(data))

        return Response(data={
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }, status=status.HTTP_200_OK)






############################# ADDITIONAL APIs FOR FUTURE INTEGRATION PURPOSES #########################################
    @action(methods=['POST'], detail=False, permission_classes=[
        IsAuthenticated,
    ])
    def filterByDate(self, request):

        startDate = request.data['startDate']
        endDate = request.data['endDate']
        if startDate > endDate:
            return Response({"message": "Start date cannot be before end date"}, status.HTTP_400_BAD_REQUEST)

        if endDate is None or len(endDate) == 0:
            endDate = datetime.now()

        if startDate is None or len(endDate) == 0:
            return Response({"message": "Please specify a start date"}, status.HTTP_400_BAD_REQUEST)

        queryset = Accounts.objects.filter(date__range=[startDate, endDate])
        serializer = DataSerializer(queryset, many=True)

        if len(serializer.data) == 0:
            return Response({"message": "No transaction records found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[
        AllowAny,
    ])
    def filterByType(self, request):

        accType = request.data['type']

        if accType is None or len(accType) == 0:
            return Response({"message": "Invalid transaction type"}, status.HTTP_400_BAD_REQUEST)

        queryset = Accounts.objects.filter(accountType=accType)
        serializer = DataSerializer(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[
        AllowAny,
    ])
    def filterByAccName(self, request):
        accname = request.data['accountName']

        if accname is None or len(accname) == 0:
            return Response({"message": "Account Name cannot be blank"}, status.HTTP_400_BAD_REQUEST)

        queryset = Accounts.objects.filter(accountName=accname)
        serializer = DataSerializer(queryset, many=True)

        if len(serializer.data) == 0:
            return Response({"message": "No matching account name found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
