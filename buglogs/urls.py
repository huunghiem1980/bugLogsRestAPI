from django.conf.urls import url
from buglogs import views

urlpatterns = [
    url(r'^api/logs/$', views.log_list),
    # url(r'^api/(?P<project>\w+)/logs/$', views.log_list),
    url(r'^api/logs/(?P<project>\w+)/$', views.log_list),
    url(r'^api/logs/(?P<pk>[0-9]+)$', views.log_detail),
    url(r'^api/projects/$', views.project_list),
    # url(r'^api/statistic/$', views.projectStatistic),
    url(r'^api/statistic/(?P<project>\w+)/$', views.projectStatistic),
]
