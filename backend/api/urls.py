from django.conf.urls import include, url 
from django.contrib import admin

urlpatterns = [ 
    # Examples:
    url(r'^board','api.views.dashboard_insert', name="dashboard_insert"),
    url(r'^upload/','api.views.upload', name="upload"),
    url(r'^by_volume/', 'api.views.volume', name="volume"),
    url(r'^user_data/', 'api.views.user_data', name="user_data"),
    url(r'^from_to/', 'api.views.from_to', name="from_to"),

]
