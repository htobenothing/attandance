from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns=[
    url(r'^create/$',views.create,name='create'),
    url(r'^saveall/$',views.saveAll, name='saveall')
]