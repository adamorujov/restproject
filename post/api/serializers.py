from rest_framework import serializers
from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = "post:detail",
        lookup_field = "slug"
    )
    username = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_username(self, obj):
        return obj.user.username