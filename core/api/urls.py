from django.urls import path,include
from django.conf import settings
from .views import ItemListAPIView, ItemAPIDetailView, OrderStatusListAPIView


urlpatterns = [
    # path('accounts/', include('allauth.urls')),
    path('order_status/', OrderStatusListAPIView.as_view()),

    path('items/', ItemListAPIView.as_view()),
    path('items/<pk>/', ItemAPIDetailView.as_view()),

]