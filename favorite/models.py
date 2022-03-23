from django.db import models
from django.contrib.auth.models import User
from post.models import Post

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_favorites")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_favorites")
    

