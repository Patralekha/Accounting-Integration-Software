from django.urls import path,include
from . import views
from rest_framework import routers
from .views import AuthViewSet,UserViewSet
from rest_framework import renderers



router = routers.DefaultRouter()
router.register('', AuthViewSet, basename='auth')
router.register('', UserViewSet, basename='users')


urlpatterns = router.urls