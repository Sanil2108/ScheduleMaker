import datetime
import base64

from django.db import models

TOKEN_MAX_ALLOWED_SECONDS = 1000000

class Token(models.Model):
  token_string = models.CharField(max_length = 100, primary_key = True)
  last_used_time = models.DateTimeField(auto_now=True)

  def update(self):
    self.save()

  def is_expired(self):
    return datetime.datetime.now().timestamp() - self.last_used_time.timestamp() > TOKEN_MAX_ALLOWED_SECONDS

  @staticmethod
  def create_token():
    temp_token_string = None
    while(True):
      temp_token_string = Token.get_random_token_string(100)
      token_string_already_exists = Token.objects.filter(token_string = temp_token_string).count() > 0
      if not token_string_already_exists:
        break

    token = Token()
    token.token_string = temp_token_string
    return token

  @staticmethod
  def get_random_token_string(length):
    import random

    token_string = ''
    available_char_values = []

    available_char_values.extend(list(range(65, 91)))
    available_char_values.extend(list(range(97, 123)))
    available_char_values.extend(list(range(48, 58)))

    for i in range(length):
      token_string += chr(available_char_values[int(random.random() * len(available_char_values))])
    
    return token_string

class UserManager(models.Manager):
  def get_users_starting_with_prefix(self, prefix):
    return self.filter(name__icontains = prefix)

  def get_user_with_email(self, email):
    if self.filter(email = email).count() == 1:
      return self.get(email = email)
    return None

  def get_auth_user_with_token(self, auth_header_value):
    if auth_header_value == None:
      return None

    email_token = base64.b64decode(auth_header_value.split(' ')[1]).decode('UTF-8').split(':')
    email = email_token[0]
    token = email_token[1]

    actual_user = self.get_user_with_email(email)

    if actual_user is not None and actual_user.token.token_string == token and not actual_user.token.is_expired():
      return actual_user
    return None

  def get_auth_user_with_password(self, auth_header_value):
    if auth_header_value == None:
      return None

    email_password = base64.b64decode(auth_header_value.split(' ')[1]).decode('UTF-8').split(':')
    email = email_password[0]
    password = email_password[1]

    actual_user = self.get_user_with_email(email)
    if actual_user is not None and actual_user.password == password:
      return actual_user
    return None

class User(models.Model):
  email = models.EmailField(primary_key = True)
  password = models.CharField(max_length = 100)
  name = models.CharField(max_length = 100)
  token = models.OneToOneField(Token, on_delete = models.CASCADE, blank = True, null = True)

  objects = UserManager()

  def get_complete_user(self):
    return User.objects.get_user_with_email(self.email)

  def create_token(self):
    new_token = Token.create_token()
    new_token.save()

    self.token = new_token

  def update_and_get_token(self):
    if self.token is None:
      self.create_token()
    elif self.token.is_expired():
      self.token.delete()
      self.create_token()
    else:
      self.token.update()

    self.save()
    return self.token

  def validate_password(self):
    # TODO: In future, this could have checks such as minimum length of the password and usage of
    # capital letters or numbers.
    return True

  def is_auth(self):
    try:
      actual_user = User.objects.get_user_with_email(self.email)
      if self.password == actual_user.password:
        return True
      if self.token == actual_user.token and not self.token.is_expired():
        return True
    except Exception as e:
      print(e)
      return False
    return False

  def __str__(self):
    return self.email
