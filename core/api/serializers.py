from rest_framework import serializers

from core.models import Item

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