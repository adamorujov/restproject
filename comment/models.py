from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from post.models import Post

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    content = models.TextField()
    created = models.DateTimeField(editable=False)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        self.created = timezone.now()
        super(Comment, self).save(*args, **kwargs)

