from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField()
    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(editable=False, default=timezone.now)
    slug = models.SlugField(unique=True, max_length=150, editable=False)
    image = models.ImageField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def get_slug(self):
        slug = slugify(self.title)
        unique = slug
        num = 1

        while Post.objects.filter(slug=unique).exists():
            unique = "{}-{}".format(slug, num)
            num += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
            self.slug = self.get_slug()
        self.modified = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title