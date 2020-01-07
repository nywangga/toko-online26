from django.contrib import admin
from django.urls import path,include



from .views import (
        HomeView,
        ProductView,
        CheckoutView,
        add_to_cart,
        OrderSummaryView,
        remove_from_cart,
        remove_one_from_cart,
        PaymentView,
        SearchResultsView,
        AddCouponView,
        DelCouponView,
        AddressView,
        set_def_address,
        del_address,
        AddCourier,
        SortResultsView,
        simple_checkout,
        update_transaction,
        OrderAllView,
        )



app_name = 'core'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', ProductView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-one-from-cart/<slug>/', remove_one_from_cart, name='remove-one-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('sort/', SortResultsView.as_view(), name='sort-results'),
    path('cekout/', simple_checkout, name='cekout'),
    path('update-transaction/', update_transaction, name='update-transaction'),
    path('order-history/', OrderAllView.as_view(), name='order-all'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('del-coupon/', DelCouponView.as_view(), name='del-coupon'),
    path('address/', AddressView.as_view(), name='address'),
    path('set-default-address/<pk>/', set_def_address, name='set-default-address'),
    path('delete-address/<pk>/', del_address, name='delete-address'),
    path('add-courier/', AddCourier.as_view(), name='add-courier'),


]

