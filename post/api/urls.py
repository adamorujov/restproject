from django.urls import path
from post.api import views

app_name="post"
urlpatterns = [
    path('list/', views.PostListAPIView.as_view(), name="list"),
    path('detail/<slug>/', views.PostRetrieveAPIView.as_view(), name="detail"),
    path('update/<slug>/', views.PostUpdateAPIView.as_view(), name="update"),
    path('delete/<slug>/', views.PostDestroyAPIView.as_view(), name="delete"),
    path('create/', views.PostCreateAPIView.as_view(), name="create"),
]
