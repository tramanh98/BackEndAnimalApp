from django.contrib import admin
from .models import Article, Comment, ClassAnimal, VoteArticle, LikeDislikeComment, UserFollowAnimal
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(ClassAnimal)
admin.site.register(VoteArticle)
admin.site.register(LikeDislikeComment)
admin.site.register(UserFollowAnimal)