from rest_framework import serializers

from core.models import Item, OrderStatus

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'category',
            'label',
            'price',
            'discount_price',
            'slug',
            'image',
        ]
        read_only_fields = [
            'user'
        ]


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = [
            "transaction_id",
            "order_id",
            "gross_amount",
            "payment_type",
            "transaction_time",
            "transaction_status",
            "fraud_status",
            "masked_card",
            "status_code",
            "bank",
            "status_message",
            "approval_code",
            "channel_response_code",
            "channel_response_message",
            "currency",
            "card_type",
        ]
        read_only_fields = [
            'user'
        ]