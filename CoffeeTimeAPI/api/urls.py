from django.urls import path
from .views import (
    TelegramAuthView,
    CoffeeListView,
    AddonListView,
    UserOrderListView,
    CreateOrderView,
    )
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView


schema_view = get_schema_view(
    openapi.Info(
        title="CoffeeTime API",
        default_version='v1',
        description="API для заказа кофе через Telegram",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("auth/telegram/", TelegramAuthView.as_view(), name="telegram-auth"),
    path("coffees/", CoffeeListView.as_view(), name="coffee-list"),
    path("addons/", AddonListView.as_view(), name="addon-list"),
    path("orders/", UserOrderListView.as_view(), name="user-orders"),
    path("orders/create/", CreateOrderView.as_view(), name="create-order"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
