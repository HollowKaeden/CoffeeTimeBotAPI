from rest_framework import serializers
from .models import Coffee, Addon, Order, OrderItem


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = "__all__"


class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    coffee = CoffeeSerializer()
    addons = AddonSerializer(many=True)

    class Meta:
        model = OrderItem
        fields = ['coffee', 'addons']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items']


class CreateOrderItemSerializer(serializers.Serializer):
    coffee = serializers.PrimaryKeyRelatedField(queryset=Coffee.objects.all())
    addons = serializers.PrimaryKeyRelatedField(queryset=Addon.objects.all(),
                                                many=True, required=False)


class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
        user = self.context['user']
        order = Order.objects.create(user=user)

        for item_data in validated_data['items']:
            coffee = item_data['coffee']
            addons = item_data.get('addons', [])
            order_item = OrderItem.objects.create(order=order, coffee=coffee)
            order_item.addons.set(addons)

        return order
