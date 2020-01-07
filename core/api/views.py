from rest_framework import generics, mixins, permissions
from django.shortcuts import get_object_or_404
import json
# from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
# from accounts.api.permissions import IsOwnerOrReadOnly
from .serializers import ItemSerializer, OrderStatusSerializer
from core.models import Item, OrderStatus

class ItemAPIDetailView(mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]# IsOwnerOrReadOnly]
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    # lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ItemListAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ItemSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        print(request.user)
        qs = Item.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()



class OrderStatusAPIDetailView(mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]# IsOwnerOrReadOnly]
    serializer_class = OrderStatusSerializer
    queryset = OrderStatus.objects.all()
    # lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class OrderStatusListAPIView(
    mixins.CreateModelMixin,
    generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrderStatusSerializer
    passed_id = None

    def get_queryset(self):
        request = self.request
        print(request.user)
        qs = OrderStatus.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()