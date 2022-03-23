from django.urls import path 
from favorite.api.views import FavoriteListAPIView, FavoriteCreateAPIView, FavoriteRetrieveUpdateDestroyAPIView

app_name = "favorite"

urlpatterns = [
    path('list/', FavoriteListAPIView.as_view(), name="list"),
    path('create/', FavoriteCreateAPIView.as_view(), name="create"),
    path('retrieve-update-destroy/<pk>', FavoriteRetrieveUpdateDestroyAPIView.as_view(), name="retrieve-update-destroy"),
]
