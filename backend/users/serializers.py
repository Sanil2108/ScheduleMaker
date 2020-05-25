from rest_framework import serializers

from users.models import User, Token

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=100, required = False)
  name = serializers.CharField(max_length=100, required = False)
  token = serializers.PrimaryKeyRelatedField(queryset=Token.objects.all(), required = False)
  email = serializers.EmailField(max_length=254)

  class Meta():
    model = User
    fields = ['email', 'password', 'name', 'token']

  def get_existing(self):
    return User.objects.get_user_with_email(self.validated_data['email'])

  def create(self, validated_data = None):
    if not validated_data:
      validated_data = self.validated_data
    return User(**validated_data)