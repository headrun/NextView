from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    #url(r'^board','api.views.dashboard_insert', name="dashboard_insert"),
    url(r'^error_board','api.views.error_insert', name="error_insert"),
    #url(r'^upload/','api.views.upload', name="upload"),
    #url(r'^upload/','api.views.upload', name="upload"),
    url(r'^upload/','api.views.upload_new', name="upload_new"),
    #url(r'^by_volume/', 'api.views.volume', name="volume"),
    url(r'^user_data/', 'api.views.user_data', name="user_data"),
    url(r'^from_to/', 'api.views.from_to', name="from_to"),
    url(r'^project/', 'api.views.project', name="project"),
    url(r'^chart_data/', 'api.views.chart_data', name="chart_data"),
    url(r'^yesterdays_data/', 'api.views.yesterdays_data', name="yesterdays_data"),
    url(r'^dropdown_data/', 'api.views.dropdown_data', name="dropdown_data"),
    url(r'^annotations/$', 'api.views.get_annotations', name='get_annotations'),
    url(r'^annotations/create/$', 'api.views.add_annotation', name='add_annotation'),
    url(r'^annotations/update/$', 'api.views.update_annotation', name='update_annotation'),
    #url(r'^error_upload/','api.views.error_upload', name="error_upload"),
    #url(r'^def_display/', 'api.views.default_display', name="default_display"),

]
