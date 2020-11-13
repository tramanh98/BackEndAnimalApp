from django.conf.urls import url
from django.urls import path, include

from . import views
from .views import *

app_name = 'blogPost'

urlpatterns = [
    path('api/get/user/', GetAllPost.as_view()), # Get all user's post and user's infor

    path('api/filter/animalclass/article/', FilterArticleClassAnimalView.as_view()),
    path('api/filter/article/', FilterArticles.as_view()), # Sort list

    path('api/get/article/<pk>/', ArticleDetail.as_view()), # Lấy chi tiết bài báo cùng với bình luận, tên ng đăng, 
    path('api/create/article/', CreateArticleViews.as_view()), 
    path('api/update/article/<int:id>/', ArticleUpdate.as_view()), # Update method
    path('api/delete/article/<pk>/', ArticleDelete.as_view()), # Delete method

    path('api/write/comment/', WriteComment.as_view()),
    path('api/update/comment/<int:id>/', UpdateComment.as_view()),
    path('api/delete/comment/<pk>/', DeleteComment.as_view()),

    path('api/vote/article/', VoteArticle.as_view()),
    path('api/vote/comment/', VoteComment.as_view()),
    path('api/delete/vote/comment/<pk>/', DeleteVoteComment.as_view()),
    path('api/delete/vote/article/<pk>/', DeleteVoteArticle.as_view()),

    path('api/latest/article/', ArticleListLatest.as_view()), # Get list latest
    path('api/popular/article/', ArticleListPopular.as_view()),
    path('api/trending/article/', ArticleListTrend.as_view()),

    path('api/follow/animal/', UserFollowAnimal.as_view()),
    path('api/unfollow/animal/<pk>/', UserUnfollowAnimal.as_view()), # pk là id của user 
    path('api/get/followingtag/<pk>/', GetAllTagFollow.as_view()),  # pk là id của user 
]