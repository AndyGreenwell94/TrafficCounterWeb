from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    url(r'^$',
        views.index, name='index'),

    url(r'^(?P<camera_id>[0-9]+)/$',
        views.detail, name='detail'),

    url(r'^(?P<camera_id>[0-9]+)/zone/add/$',
        login_required(views.ZoneCreate.as_view()), name='zoneCreate'),

    url(r'^(?P<camera_id>[0-9]+)/zone/(?P<zone_id>[0-9]+)/$',
        login_required(views.ZoneUpdate.as_view()), name='zoneUpdate'),

    url(r'^(?P<camera_id>[0-9]+)/zone/(?P<zone_id>[0-9]+)/delete/$',
        login_required(views.ZoneDelete.as_view()), name='zoneDelete'),

    url(r'^(?P<camera_id>[0-9]+)/zone/(?P<zone_id>[0-9]+)/zoneop/add/$',
        views.ZoneOptionCreate.as_view(), name='zoneopCreate'),

    url(r'^(?P<camera_id>[0-9]+)/zone/(?P<zone_id>[0-9]+)/zoneop/(?P<zoneop_id>[0-9]+)/$',
        views.ZoneOptionsUpdate.as_view(), name='zoneopUpdate'),

    url(r'^(?P<camera_id>[0-9]+)/zone/(?P<zone_id>[0-9]+)/zoneop/(?P<zoneop_id>[0-9]+)/delete$',
        views.ZoneOptionsUpdate.as_view(), name='zoneopDelete'),

    url(r'^(?P<camera_id>[0-9]+)/timetable/add/$',
        views.TimeTableCreate.as_view(), name='timetableCreate'),

    url(r'^(?P<camera_id>[0-9]+)/timetable/(?P<timetable_id>[0-9]+)/$',
        views.TimeTableUpdate.as_view(), name='timetableUpdate'),

    url(r'^(?P<camera_id>[0-9]+)/timetable/(?P<timetable_id>[0-9]+)/delete$',
        views.timetable_delete, name='timetableDelete')
]

