from django.conf.urls import  url
from django. urls import include, path
from . import views
from rest_framework import renderers
from rest_framework import routers
from .views import XFunctionsViewSet

router = routers.DefaultRouter()

router.register('',XFunctionsViewSet, basename='xfunctions')

urlpatterns = router.urls

urlpatterns += [

     path('xero', views.xero, name='xero'),
      path('xero_callback', views.xero_callback, name='xero_callback'),
      path('xeroData',views.fetchXeroData,name='xeroData')
]
