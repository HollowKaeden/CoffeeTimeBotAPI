import json
from urllib.parse import parse_qsl
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import TelegramUser, Coffee, Addon, Order
from .utils.telegram_auth import verify_telegram_auth
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    CoffeeSerializer,
    AddonSerializer,
    OrderSerializer,
    CreateOrderSerializer,
)
from django.conf import settings
from jwt import decode, InvalidTokenError


class TelegramAuthView(APIView):
    """
    Принимает POST с JSON: {"init_data": "<строка initData>"}
    Возвращает JWT access-токен при успешной верификации.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        init_data = request.data.get('init_data')
        if not init_data or not verify_telegram_auth(init_data):
            return Response(
                {"detail": "Invalid Telegram auth"},
                status=status.HTTP_403_FORBIDDEN
            )
        # Разбираем init_data для получения user-поля
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
        user_json = parsed.get('user')
        if not user_json:
            return Response(
                {"detail": "Missing user data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user_info = json.loads(user_json)

        user, _ = TelegramUser.objects.get_or_create(
            telegram_id=str(user_info["id"]),
            defaults={
                "first_name": user_info.get("first_name", ""),
                "username": user_info.get("username", ""),
            }
        )
        # Генерируем JWT-токен
        refresh_token = RefreshToken.for_user(user)
        return Response({"access": str(refresh_token.access_token),
                         "refresh": str(refresh_token)})


class CoffeeListView(generics.ListAPIView):
    queryset = Coffee.objects.all()
    serializer_class = CoffeeSerializer
    permission_classes = [permissions.AllowAny]


class AddonListView(generics.ListAPIView):
    queryset = Addon.objects.all()
    serializer_class = AddonSerializer
    permission_classes = [permissions.AllowAny]


def get_user_id_from_request(request):
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            decoded = decode(token, settings.SECRET_KEY,
                             algorithms=["HS256"])
            return decoded.get('user_id')
        except InvalidTokenError:
            return None
    return None


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = get_user_id_from_request(self.request)
        user = TelegramUser.objects.get(pk=user_id)

        return Order.objects.filter(user=user)


class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_id = get_user_id_from_request(self.request)
        user = TelegramUser.objects.get(pk=user_id)
        serializer.context['user'] = user
        serializer.save(user=user)
