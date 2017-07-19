from django.views import generic
from django.conf.urls import url, include

from . import views

app_name = 'survey'
urlpatterns = [
    url(r'^review_data/$', views.review_data, name='review_data'),
    url(r'^export_report_data/$', views.export_report_data, name='export_report_data'),
    url(r'^export_attendance_data/$', views.export_attendance_data, name='export_attendance_data'),
    url(r'^export_video_data/$', views.export_video_data, name='export_video_data'),
    url(r'^survey/$', views.survey_form, name='survey'),
    url(r'^$', views.survey_form),
    url(r'^video/$', views.video, name='video'),
    url(r'^attendance/$', views.attendance, name='attendance'),
    url(r'^no_sd_card/$', views.no_sd_card, name='no_sd_card'),
    url(r'^time_is_off/$', views.time_is_off, name='time_is_off'),
]
