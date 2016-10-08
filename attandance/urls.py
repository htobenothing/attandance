from django.conf.urls import url,include
from attandance import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns=[
    url(r'^create/$',views.create,name='create'),
    url(r'^saveall/$',views.saveAll, name='saveall'),
    url(r'^members/$',views.MemberList.as_view()),
    url(r'^members/(?P<pk>[0-9]+)/$',views.MemberDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)