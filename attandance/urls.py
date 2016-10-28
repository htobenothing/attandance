from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from attandance import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns=[
    url(r'^create/$',views.create, name='create'),
    url(r'^saveall/$',views.saveAll, name='saveall'),
    url(r'^sendEmail/$',views.sendEmailToChurchOffice,name='sendEmail'),

    url(r'^$',views.IndexView.as_view(), name='index'),
    url(r'^login/$',views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),


    url(r'^members/$', views.MemberList.as_view()),
    url(r'^members/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view()),
    url(r'^attandancehistorys/$', views.AttandanceHistoryList.as_view()),
    url(r'^attandancehisorys/(?P<pk>[0-9]+)/$', views.AttandanceHistoryDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)