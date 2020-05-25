from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from schedule.serializers import ScheduleSerializer, CommentSerializer, EventSerializer, DatesSerializer
from schedule.models import Schedule, Event, Category

from users.models import User

class UserScheduleDateListView(APIView):
  def get(self, request):
    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user is None:
      return Response('No such user exists', status = status.HTTP_401_UNAUTHORIZED)

    dates_serializer = DatesSerializer(data = {'dates': request.query_params.get('dates').split(',')})
    dates_serializer.is_valid(raise_exception = True)

    dates = dates_serializer.create()

    many_schedule_serializers = ScheduleSerializer(
      Schedule.objects.get_schedules_by_date(user, dates),
      many = True
    )

    return Response(many_schedule_serializers.data, status = status.HTTP_200_OK)

class ScheduleListView(APIView):
  def get(self, request):
    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))

    many_schedule_serializers = ScheduleSerializer(
      Schedule.objects.get_all_visible_to_user(user),
      many = True
    )

    return Response(many_schedule_serializers.data, status = status.HTTP_200_OK)

class ScheduleView(APIView):
  def patch(self, request, schedule_id):
    if schedule_id is None or Schedule.objects.filter(pk = schedule_id).count() is 0:
      return Response(status = status.HTTP_400_BAD_REQUEST)

    schedule = Schedule.objects.get(pk = schedule_id)
    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user is not None and schedule in list(user.schedule_set.all()):
      shared_users_emails = request.data['shared_to']
      public_enabled = request.data['public']

      schedule.update_sharing(shared_users_emails = shared_users_emails, public_enabled = public_enabled)

      return Response(ScheduleSerializer(schedule).data, status = status.HTTP_200_OK)
    else:
      return Response(status = status.HTTP_403_FORBIDDEN)

  def delete(self, request, schedule_id = None):
    if schedule_id is None or Schedule.objects.filter(pk = schedule_id).count() is 0:
      return Response(status = status.HTTP_400_BAD_REQUEST)

    schedule = Schedule.objects.get(pk = schedule_id)
    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user is not None and schedule in list(user.schedule_set.all()):
      schedule.delete()
      return Response(status = status.HTTP_200_OK)
    else:
      return Response(status = status.HTTP_403_FORBIDDEN)

  def get(self, request, schedule_id = None):
    if schedule_id is None or Schedule.objects.filter(pk = schedule_id).count() is 0:
      return Response('No such schedule', status = status.HTTP_400_BAD_REQUEST)

    schedule = Schedule.objects.get(pk = schedule_id)
    if schedule.public:
      return Response(ScheduleSerializer(schedule).data, status = status.HTTP_200_OK)
    else:
      user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
      if user is not None and schedule.is_visible_to_user(user):
        return Response(ScheduleSerializer(schedule).data, status = status.HTTP_200_OK)
      else:
        return Response(status = status.HTTP_403_FORBIDDEN)

  def post(self, request, schedule_id = None):
    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user is None:
      return Response(status = status.HTTP_401_UNAUTHORIZED)

    scheduleSerializer = ScheduleSerializer(data = request.data['schedule'])
    scheduleSerializer.is_valid(raise_exception = True)
    schedule = scheduleSerializer.create()
    schedule.owner = user

    try:
      schedule.save()
    except Exception as e:
      print(e)
      return Response(status = status.HTTP_400_BAD_REQUEST)

    return Response(ScheduleSerializer(schedule).data, status = status.HTTP_201_CREATED)

class EventView(APIView):

  def patch(self, request, schedule_id, event_id):
    if Event.objects.filter(pk = event_id).count() == 0:
      return Response('Event does not exist', status = status.HTTP_404_NOT_FOUND)

    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user == None:
      return Response(status = HTTP_401_UNAUTHORIZED)

    schedule = Schedule.objects.get(pk = schedule_id)
    if user is not None and schedule not in list(user.schedule_set.all()):
      return Response(status = status.HTTP_403_FORBIDDEN)

    event = Event.objects.get(pk = event_id)
    if event is not None and event not in list(schedule.event_set.all()):
      return Response(status = status.HTTP_403_FORBIDDEN)
    
    event_serializer = EventSerializer(data = request.data)
    event_serializer.is_valid(raise_exception = True)
    overriding_event = event_serializer.create()
    event.override(overriding_event)

    return Response(EventSerializer(event).data, status = status.HTTP_200_OK)

  def delete(self, request, schedule_id, event_id):
    if Event.objects.filter(pk = event_id).count() == 0:
      return Response('Event does not exist', status = status.HTTP_404_NOT_FOUND)

    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user == None:
      return Response(status = HTTP_401_UNAUTHORIZED)

    schedule = Schedule.objects.get(pk = schedule_id)
    if user is not None and schedule not in list(user.schedule_set.all()):
      return Response(status = status.HTTP_403_FORBIDDEN)

    event = Event.objects.get(pk = event_id)
    if event is not None and event not in list(schedule.event_set.all()):
      return Response(status = status.HTTP_403_FORBIDDEN)
    
    event.delete()
    return Response(status = status.HTTP_200_OK)

  def post(self, request, schedule_id, event_id = None):
    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user == None:
      return Response(status = HTTP_401_UNAUTHORIZED)

    schedule = Schedule.objects.get(pk = schedule_id)
    if user is not None and schedule not in list(user.schedule_set.all()):
      return Response(status = status.HTTP_403_FORBIDDEN)

    event_serializer = EventSerializer(data = request.data)
    event_serializer.is_valid(raise_exception = True)
    event = event_serializer.create()
    event.schedule = schedule
    event.save()

    schedule.event_set.add(event)
    schedule.save()

    return Response(EventSerializer(event).data, status = status.HTTP_201_CREATED)

class CommentView(APIView):

  def post(self, request, schedule_id):
    user = User.objects.get_auth_user_with_token(request.META.get('HTTP_AUTHORIZATION'))
    if user == None:
      return Response(status = HTTP_401_UNAUTHORIZED)
    
    schedule = Schedule.objects.get(pk = schedule_id)
    if not schedule.is_visible_to_user(user):
      return Response(status = status.HTTP_403_FORBIDDEN)

    comment_serializer = CommentSerializer(data = request.data)
    comment_serializer.is_valid(raise_exception = True)
    comment = comment_serializer.create()
    comment.user = user
    comment.schedule = schedule
    comment.save()

    schedule.comment_set.add(comment)
    schedule.save()

    return Response(CommentSerializer(comment).data, status = status.HTTP_201_CREATED)

