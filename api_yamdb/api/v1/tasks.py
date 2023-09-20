from .serializers import UserSerializer
from users.models import User
from django.contrib.auth.tokens import default_token_generator
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from celery import shared_task


@shared_task()
def create_user_send_mail(request):
    """Создает объект класса User и
    отправляет на почту пользователя код подтверждения."""

    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(**serializer.validated_data)
    email = user.email
    confirmation_code = default_token_generator.make_token(user)

    send_mail(subject='Код подтверждения',
              message=f'Your code: {confirmation_code}',
              from_email=DEFAULT_FROM_EMAIL,
              recipient_list=(email,))

    return Response(serializer.data, status=status.HTTP_200_OK)
