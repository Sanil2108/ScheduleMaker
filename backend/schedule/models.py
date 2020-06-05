import datetime
import random

from django.db import models
from django.db.models import Q

from users.models import User

category_colors = [
  '#ab47bc',
  '#673ab7',
  '#1e88e5',
  '#f44336',
  '#43a047',
  '#f57c00',
  '#ff7043'
]

class ScheduleManager(models.Manager):
  def get_all_visible_to_user(self, user):
    if user is None:
      return list(Schedule.objects.filter(public = True))
    return list(set(list(Schedule.objects.filter(Q(public = True) | Q(owner = user)).filter(date__gte = datetime.datetime.now())) + list(user.schedule_set.all()) + list(user.shared_schedules.all())))
  
  def get_schedules_by_date(self, user, dates):
    return list(user.schedule_set.filter(date__in = dates))    

class Schedule(models.Model):
  name = models.CharField(max_length = 100, blank = True, null = True)
  date = models.DateField()
  owner = models.ForeignKey(User, on_delete = models.CASCADE)
  public = models.BooleanField(default = False)
  shared_to = models.ManyToManyField(User, related_name = 'shared_schedules')

  objects = ScheduleManager()

  class Meta:
    unique_together = ('owner', 'date')

  def update_sharing(self, shared_users_emails = None, public_enabled = None):
    if public_enabled is not None:
      self.public = public_enabled
    if shared_users_emails is not None:
      self.shared_to.set(shared_users_emails)
    self.save()

  def is_visible_to_user(self, user):
    all_visible_schedules = Schedule.objects.get_all_visible_to_user(user)
    for visible_schedule in all_visible_schedules:
      if self.id == visible_schedule.id:
        return True
    return False
  
  def __str__(self):
    return 'Schedule created by {owner} on {date}'.format(date = self.date, owner = self.owner)

class CategoryManager(models.Manager):
  def get_or_create(self, category_text):
    if self.filter(pk = category_text).count() == 1:
      return self.get(pk = category_text)
    else:
      category = Category()
      category.name = category_text
      category.set_random_colour()
      category.save()
      return category

class Category(models.Model):
  name = models.CharField(max_length = 100, primary_key = True)
  color = models.CharField(max_length = 10)

  objects = CategoryManager()

  def set_random_colour(self):
    self.color = category_colors[random.randint(0, len(category_colors) - 1)]

  def __str__(self):
    return self.name

class Event(models.Model):
  title = models.CharField(max_length = 100)
  description = models.CharField(max_length = 100, blank = True, null = True)
  category = models.ForeignKey(Category, on_delete = models.CASCADE)
  schedule = models.ForeignKey(Schedule, on_delete = models.CASCADE)
  start_time = models.TimeField()
  end_time = models.TimeField()

  def override(self, overriding_event):
    if hasattr(overriding_event, 'description') and overriding_event.description is not None:
      self.description = overriding_event.description
    if hasattr(overriding_event, 'start_time') and overriding_event.start_time is not None:
      self.start_time = overriding_event.start_time
    if hasattr(overriding_event, 'end_time') and overriding_event.end_time is not None:
      self.end_time = overriding_event.end_time
    
    self.save()
    
class Comment(models.Model):
  comment_text = models.CharField(max_length = 300)
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  creation_time = models.DateTimeField(auto_now_add=True)
  schedule = models.ForeignKey(Schedule, on_delete = models.CASCADE)

  class Meta():
    ordering = ['creation_time']

  def __str__(self):
    return '{comment_text} by {user}'.format(comment_text = self.comment_text, user = self.user)
