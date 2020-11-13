from django.db import models

# Create your models here.
from django.utils import timezone
from user.models import User

ANIMAL_CLASS = (
    ('A', 'Bò sát'),
    ('B', 'Chân khớp'),
    ('C', 'Thú'),
    ('D', 'Chim'),
    ('E', 'Côn trùng')
)

class ClassAnimal (models.Model):
    name = models.CharField(max_length=255)

class Article(models.Model):
    user = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)  # Tiêu đề bài viết
    image = models.URLField()
    content = models.TextField(null=True, blank=True)  # Nội dung bài viết
    typeClass = models.ForeignKey(ClassAnimal, related_name='articles', on_delete=models.CASCADE)  # Loai
    dangerous = models.BooleanField(default=True)
    underwater = models.BooleanField(default=True)
    terrestrial= models.BooleanField(default=True)
    pets = models.BooleanField(default=True)
    wild = models.BooleanField(default=True)
    rare = models.BooleanField(default=True)
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    comment = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    def __str__(self):
        return self.title

class Comment (models.Model):
    user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments',on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)  # Nội dung comment
    like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)


VOTE_TYPE = (
    ('1', 'VOTE'),
    ('2', 'Normal')
)

# if unvote, 1 row will be delete, 3 method are get, create and delete 
class VoteArticle (models.Model):
    user = models.ForeignKey(User, related_name='voteArticle', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='votes',on_delete=models.CASCADE)
    vote = models.CharField(max_length=1, choices=VOTE_TYPE, default='1', db_index=True)  # Quận

LIKE_DISLIKE = (
    ('0', "Normal"),
    ('1', "Like")
)
class LikeDislikeComment (models.Model):
    user = models.ForeignKey(User, related_name='expressing', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='votes',on_delete=models.CASCADE)
    vote = models.CharField(max_length=1, choices=LIKE_DISLIKE, default='0', db_index=True)  # Quận


class UserFollowAnimal (models.Model):
    user = models.ForeignKey(User, related_name='followingtag', on_delete=models.CASCADE)
    animal = models.ForeignKey(ClassAnimal, related_name='followed',on_delete=models.CASCADE)
