"""cogsg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from attandance import views


router = routers.SimpleRouter()
# router.register(r'users',views.UserViewSet)
router.register(r'accounts',views.AccountViewSet)
router.register(r'groups',views.GroupViewset)
router.register(r'members',views.MemberViewSet)
router.register(r'attandancehistory',views.AttandanceHistoryViewSet)

urlpatterns = [
    url(r'^attandance/', include('attandance.urls',namespace='attan')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/',include(router.urls)),
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^auth/',include('rest_framework_social_oauth2.urls'))
    url(r'^api/',include('rest_framework.urls'))
]



