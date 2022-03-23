from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from comment.models import Comment
from comment.api.serializers import CommentListSerializer, CommentCreateSerializer, CommentDestroyUpdateSerializer
from comment.api.permissions import IsOwner
from comment.api.paginations import CommentPagination

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        query = self.request.GET.get("q")
        if query:
            queryset = Comment.objects.filter(parent=None).filter(post=query)
        return queryset
    

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDestroyUpdateSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

