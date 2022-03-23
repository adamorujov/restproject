from django.contrib.auth.models import User
from rest_framework import serializers
from favorite.models import Favorite
from post.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

class FavoriteListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Favorite
        fields = "__all__"

class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"

    def validate(self, data):
        queryset = Favorite.objects.filter(user=data["user"], post=data["post"])
        if queryset.exists():
            raise serializers.ValidationError("This post has been added already.")
        return data

class FavoriteRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"
