from django.urls import path,include
from django.conf import settings
from .views import ItemListAPIView, ItemAPIDetailView


urlpatterns = [
    # path('accounts/', include('allauth.urls')),
    path('', ItemListAPIView.as_view()),
    path('<pk>/', ItemAPIDetailView.as_view())

]