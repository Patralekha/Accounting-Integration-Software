from django.conf.urls import  url
from django. urls import include, path
from . import views
from rest_framework import renderers
from rest_framework import routers
from .views import TransactionViewSet

router = routers.DefaultRouter()



urlpatterns = router.urls