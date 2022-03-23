from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from favorite.models import Favorite
from favorite.api.serializers import FavoriteListSerializer, FavoriteCreateSerializer, FavoriteRetrieveUpdateDestroySerializer
from favorite.api.permissions import IsOwner

class FavoriteListAPIView(ListAPIView):
    serializer_class = FavoriteListSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

class FavoriteCreateAPIView(CreateAPIView):
    serializer_class = FavoriteCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class FavoriteRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteRetrieveUpdateDestroySerializer
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)

