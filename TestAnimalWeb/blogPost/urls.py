from django.conf.urls import url
from django.urls import path, include
from rest_framework.permissions import IsAuthenticated, AllowAny
from . import views
from .views import *

app_name = 'blogPost'

urlpatterns = [
    # pk là ID của user 
    path('api/get/infor/user/<pk>/', GetInforOtherUser.as_view()), # Get all user's post and user's infor ==> used
    path('api/get/all/articles/', GetUserAllArticle.as_view()),  # ==> used

    # có 2 loại filter, 1 loại là filter theo ID loài, loại filter thứ 2 là lọc theo các điều kiện (vd: rare, wild,...)
    path('api/filter/animalclass/article/', FilterArticleClassAnimalView.as_view()), # lọc theo id loài 
    path('api/filter/article/', FilterArticles.as_view()), # lọc theo điều kiện 

    path('api/get/article/<pk>/', ArticleDetail.as_view()), # Lấy chi tiết bài báo cùng với bình luận, tên ng đăng, ==>used 
    path('api/get/your/article/<pk>/', GetArticle.as_view()), # lấy dữ liệu bài viết để chỉnh sửa  ==> used
    path('api/create/article/', CreateArticleViews.as_view()),  # ==>used
    path('api/update/article/<int:id>/', ArticleUpdate.as_view()), # Update method  ==> used
    path('api/delete/article/<pk>/', ArticleDelete.as_view()), # Delete method  ==> used

    path('api/write/comment/', WriteComment.as_view()),  # ==> used
    path('api/update/comment/<int:id>/', UpdateComment.as_view()),
    path('api/delete/comment/<pk>/', DeleteComment.as_view()),
    path('api/get/comments/', GetListComment.as_view()),  # ==> used

    path('api/vote/article/', VoteArticleView.as_view()),  # ==> used
    path('api/vote/comment/', VoteComment.as_view()),  # ==> used
    path('api/delete/vote/comment/<pk>/', DeleteVoteComment.as_view()),  # ==> used
    path('api/delete/vote/article/<pk>/', DeleteVoteArticle.as_view()),  # ==> used

    path('api/latest/article/', ArticleListLatest.as_view()), # Get list latest
    path('api/popular/article/', ArticleListPopular.as_view()),
    path('api/trending/article/', ArticleListTrend.as_view()),

    path('api/follow/animal/', UserFollowAnimal.as_view()),  # used
    path('api/unfollow/animal/<pk>/', UserUnfollowAnimal.as_view()), # pk là id của user  ==> used
    path('api/get/followingtag/<pk>/', GetAllTagFollow.as_view()),  # get all tag that user follow ==> used
                                                                    #pk là id của user  
]