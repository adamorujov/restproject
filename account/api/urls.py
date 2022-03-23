from django.urls import path
from account.api.views import UserRetrieveUpdateAPIView, UpdatePasswordAPIView, RegisterAPIView

app_name = "account"

urlpatterns = [
    path('me/', UserRetrieveUpdateAPIView.as_view(), name="me"),
    path('change-password/', UpdatePasswordAPIView.as_view(), name="change-password"),
    path('create-user/', RegisterAPIView.as_view(), name="create-user"),
]

