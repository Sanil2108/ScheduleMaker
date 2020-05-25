from django.urls import path

from users.views import CreateUser, LoginUser

urlpatterns = [
    path('create/', CreateUser.as_view(), name = 'Create user'),
    path('login/', LoginUser.as_view(), name = 'Login user'),
]
