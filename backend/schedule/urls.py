from django.urls import path, re_path

from schedule.views import EventView, ScheduleView, CommentView, ScheduleListView, UserScheduleDateListView

urlpatterns = [
    path('', ScheduleView.as_view(), name = 'Schedule detail'),
    re_path(r'^(?P<schedule_id>[\d]+)/$', ScheduleView.as_view(), name = 'Schedule detail with parameter'),
    path('list/', ScheduleListView.as_view(), name = 'All schedules'),
    path('dates_list', UserScheduleDateListView.as_view(), name = 'All schedules for user based on dates'),
    re_path(r'^(?P<schedule_id>[\d]+)/events/(?P<event_id>[\d]*)$', EventView.as_view(), name = 'Events detail'),
    path('<int:schedule_id>/comments/', CommentView.as_view(), name = 'Comments detail'),
]
