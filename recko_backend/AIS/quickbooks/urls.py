from django.conf.urls import  url
from django. urls import include, path
from . import views
from rest_framework import renderers
from rest_framework import routers
from .views import QFunctionsViewSet

router = routers.DefaultRouter()

router.register('', QFunctionsViewSet, basename='qfunctions')

urlpatterns = router.urls


urlpatterns += [
   path('quickbook', views.quickbook, name='quickbook'),
    path('callback', views.callback, name='callback'),
     path('qbo', views.fetchQboData, name='qbo')
]