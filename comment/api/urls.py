from django.urls import path
from comment.api import views

app_name = "comment"
urlpatterns = [
    path('list/', views.CommentListAPIView.as_view(), name="list"),
    path('create/', views.CommentCreateAPIView.as_view(), name="create"),
    path('update/<pk>/', views.CommentUpdateAPIView.as_view(), name="update"),
]