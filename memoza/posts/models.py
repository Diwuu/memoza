from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import string, random

class Posts(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumb = models.ImageField(default='default.png', blank=True)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        if unique_slug == '':
            letters = string.ascii_lowercase
            unique_slug = ''.join(random.choice(letters) for i in range(10))
        num = 1
        while Posts.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Posts'


class Comments(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    content = models.TextField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)


    def __str__(self):
        return self.content


from django.db import models
from django.contrib.auth.models import User


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.post) + ':' + str(self.value)

    class Meta:
        unique_together = ("user", "post", "value")