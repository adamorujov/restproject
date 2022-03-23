from django.contrib.auth.models import User
from rest_framework import serializers
from post.models import Post
from comment.models import Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class CommentChildSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        if obj.replies.all():
            return CommentChildSerializer(obj.replies.all(), many=True).data

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("post", "parent", "content")

    def validate(self, data):
        if data["parent"]:
            if data["parent"].post != data["post"]:
                raise serializers.ValidationError("Something went wrong!")
        return data 

class CommentDestroyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
