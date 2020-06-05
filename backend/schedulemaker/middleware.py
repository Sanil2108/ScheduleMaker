from rest_framework.response import Response
from rest_framework import status
from django.utils.deprecation import MiddlewareMixin

class ErrorHandlerMiddleWare(MiddlewareMixin):
    def process_exception(self, request, exception):
        response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response.content = 'Unknown error'
        return response