from rest_framework import serializers

from schedule.models import Schedule, Event, Category, Comment
from users.models import User

class CommentSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required = False)
  creation_time = serializers.DateTimeField(read_only=True, required = False)

  class Meta():
    model = Comment
    fields = ['comment_text', 'user', 'creation_time']

  def create(self, validated_data = None):
    if not validated_data:
      validated_data = self.validated_data
    return Comment(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
  name = serializers.CharField(max_length=100)
  color = serializers.CharField(max_length=10, required = False)

  class Meta():
    model = Category
    fields = ['name', 'color']

class EventSerializer(serializers.ModelSerializer):
  category = CategorySerializer(required = False)
  schedule = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all(), required = False)
  start_time = serializers.TimeField(required = False)
  end_time = serializers.TimeField(required = False)
  title = serializers.CharField(max_length=100, required = False)

  class Meta():
    model = Event
    fields = ['title', 'description', 'schedule', 'start_time', 'end_time', 'category', 'id']

  def create(self, validated_data = None):
    if not validated_data:
      validated_data = self.validated_data

    complete_validated_data = validated_data.copy()
    if 'category' in validated_data:
      complete_validated_data['category'] = Category.objects.get_or_create(validated_data['category']['name'])
    return Event(**complete_validated_data)

class ScheduleSerializer(serializers.ModelSerializer):
  date = serializers.DateField()
  owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required = False)
  shared_to = serializers.PrimaryKeyRelatedField(allow_empty=True, many=True, required = False, read_only = True)
  # comment_set = serializers.SlugRelatedField(many=True, slug_field = 'comment_text', queryset = Comment.objects.all(), required = False)
  comment_set = CommentSerializer(many=True, required = False, read_only = True)
  event_set = EventSerializer(many=True, required = False, read_only = True)

  class Meta():
    model = Schedule
    fields = ['date', 'owner', 'public', 'shared_to', 'comment_set', 'event_set', 'id']
    validators = []

  def create(self, validated_data = None):
    if not validated_data:
      validated_data = self.validated_data

    return Schedule(**validated_data)

class DatesSerializer(serializers.Serializer):
  dates = serializers.ListField(child = serializers.DateField())

  def create(self, validated_data = None):
    if not validated_data:
      validated_data = self.validated_data
    return validated_data['dates']

