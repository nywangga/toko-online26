from django.contrib import admin

from .models import Item, OrderItem, Order, Address, Coupon, Courier, OrderStatus


admin.site.register(Item)

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(Courier)
admin.site.register(OrderStatus)
