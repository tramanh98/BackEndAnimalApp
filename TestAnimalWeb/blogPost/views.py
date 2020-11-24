from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from user.models import User
from .models import Article, Comment, ClassAnimal, VoteArticle, LikeDislikeComment, UserFollowAnimal
from .serializers import (ArticleSerializer , UserArticleSerializers, UserFollowAnimalSerializers,
                            AnimalArticleSerializers, TagAnimalFollowSerializers, CommentsWithVotesSerializers,
                            GetDetailArticleSerializer, ExpressCommentSerializers, 
                            VoteArticleSerializers, CommentSerializers, GetAllArticleSerializer)
from user.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, )
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination

class ArticlePagination(PageNumberPagination): #Sắp xếp bài đăng 1 page 10 trang
    page_size = 10

class CreateArticleViews(generics.CreateAPIView): #Tạo bài đăng api/create/article/
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self): #Authentication user để tạo bài đăng
        usr = User.objects.get(pk = self.request.user)
        usr.posts = usr.posts + 1
        query = Article.objects.filter(user=self.request.user)
        return query
    def perform_create(self, serializer):
        print(self.request)
        serializer.save(user=self.request.user)


class ArticleUpdate(generics.UpdateAPIView): #Cập nhật bài đăng api/motels/update/<pk>
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'
    def get_queryset(self): #Authentication user để update
        query = Article.objects.filter(user=self.request.user)
        return query


class ArticleDelete(generics.DestroyAPIView): #Xóa bài bài đăng api/motels/delete/<pk>/
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ArticleSerializer
    def get_queryset(self): #Authentication user để xóa bài đăng
        query = Article.objects.filter(user=self.request.user)
        return query

############ fix here, sử dụng tên id ng dùng để lấy thông tin user 
# class GetAllPost(APIView): # lấy tất cả thông tin user và các bài post của user đó
#     queryset = User.objects.all()
#     serializer_class = UserArticleSerializers
#     permission_classes = [IsAuthenticated]
#     @csrf_exempt
#     def get(seft, request, *args, **kwargs):
#         print(request.user.id)
#         user = get_object_or_404(User, pk = request.user.id)
#         serializer = UserArticleSerializers(user)
#         return Response({"profile": serializer.data})

class GetInforOtherUser(generics.RetrieveAPIView): # lấy tất cả thông tin user của user đó api/user/<id>
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserArticleSerializers

class GetUserAllArticle(generics.ListAPIView):  # lấy tất cả bài báo của một user nào đó 
    pagination_class = ArticlePagination
    serializer_class = GetAllArticleSerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Article.objects.all()
        idUser = self.request.query_params.get('idUser')
        queryset = queryset.filter(user = int(idUser))
        return queryset


class ArticleDetail(generics.RetrieveAPIView): #Get bài đăng để xem api/get/article/<pk>/
    permission_classes = (AllowAny,)
    queryset = Article.objects.all()
    serializer_class = GetDetailArticleSerializer
    def retrieve(self, request, *args, **kwargs):
        artc = Article.objects.get(id = int(self.kwargs.get('pk')))
        artc.view = artc.view + 1
        artc.save()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class GetArticle(generics.RetrieveAPIView): #Get bài đăng để chỉnh sửa api/acticle/<id>
    permission_classes = (AllowAny,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class OtherUserInfor(generics.RetrieveAPIView): #Get thông tin của user khác api/user/<id> , id là id của user 
    permission_classes = (AllowAny,)
    queryset = Article.objects.all()
    serializer_class = UserArticleSerializers

######################### WRITE, UPDATE, DELETE COMMENT #############################
class WriteComment(generics.CreateAPIView): # Viết bình luận
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        query = Comment.objects.filter(user=self.request.user)
        return query
    def perform_create(self, serializer):
        # tăng 1 bình luận trên 1 bài viết
        articlecm = Article.objects.get(id = int(self.request.data["article"]))
        articlecm.comment = articlecm.comment + 1
        articlecm.save()
        serializer.save(user=self.request.user)


class UpdateComment(generics.UpdateAPIView): #Cập nhật bình luận api/comment/update/<pk>
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    lookup_field = 'id'
    def get_queryset(self): 
        query = Comment.objects.filter(user=self.request.user)
        return query

class DeleteComment(generics.DestroyAPIView): #Xóa bình luận api/comment/delete/<pk>/
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializers
    def get_queryset(self): #Authentication user để xóa bài đăng
        # giảm 1 bình luânj trên 1 bài viết 
        cmt = Comment.objects.get(id = int(self.kwargs.get('pk')))
        articlecm = cmt.article
        articlecm.comment = articlecm.comment - 1  # giảm số bình luận của bài viết
        articlecm.save()
        query = Comment.objects.filter(user=self.request.user)
        return query

class GetListComment(generics.ListAPIView):  # lấy list comment của 1 bài báo 
    pagination_class = ArticlePagination
    serializer_class = CommentsWithVotesSerializers
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Comment.objects.all()
        idPost = self.request.query_params.get('idPost')
        queryset = queryset.filter(article = int(idPost))
        return queryset


########################## LIST ARTICLES #########################################
##################### lọc các bài viết theo lớp ############

class FilterArticleClassAnimalView(generics.ListAPIView):  # có 1 cách khác, dùng AnimalArticleSerializers
    pagination_class = ArticlePagination
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Article.objects.all()
        idClass = self.request.query_params.get('idClass')
        queryset = queryset.filter(typeClass=int(idClass))
        return queryset

class FilterArticles (generics.ListAPIView): # lọc theo các điều kiện true fales 
    pagination_class = ArticlePagination
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Article.objects.all()
        option = self.request.query_params.get('option')
        if option == 'danger':
            queryset = queryset.filter(dangerous = True)
        if option == 'underwater':
            queryset = queryset.filter(underwater = True)
        if option == 'terrestrial':
            queryset = queryset.filter(terrestrial = True)
        if option == 'pets':
            queryset = queryset.filter(pets = True)
        if option == 'wild':
            queryset = queryset.filter(wild = True)
        if option == 'rare':
            queryset = queryset.filter(rare = True)
        return queryset


######### fixing here 
class FilterArticleFollow (generics.ListAPIView): # lọc các bài viết thuộc lớp đv mà user theo dõi 
    pagination_class = ArticlePagination
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryClass = UserFollowAnimal.objects.filter(user=self.request.user)  # lấy các loài user quan tâm
        # sau đó lọc các bài viết theo cái loài đó 
        queryset = Article.objects.all()
        option = self.request.query_params.get('option')
        if option == 'danger':
            queryset = queryset.filter(dangerous = True)
        if option == 'underwater':
            queryset = queryset.filter(underwater = True)
        if option == 'terrestrial':
            queryset = queryset.filter(terrestrial = True)
        if option == 'pets':
            queryset = queryset.filter(pets = True)
        if option == 'wild':
            queryset = queryset.filter(wild = True)
        if option == 'rare':
            queryset = queryset.filter(rare = True)
        return queryset


class ArticleListLatest(generics.ListAPIView): # lấy các bài đăng mới nhất
    pagination_class = ArticlePagination
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Article.objects.filter().order_by('-created_at')
        return queryset

class ArticleListPopular(generics.ListAPIView): # lấy các bài đăng có nhiều lượt view nhất
    pagination_class = ArticlePagination
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Article.objects.filter().order_by('-view')
        return queryset

class ArticleListTrend(generics.ListAPIView): # lấy các bài đăng có nhiều lượt yêu thích nhất
    pagination_class = ArticlePagination
    serializer_class = ArticleSerializer
    permission_classes = (AllowAny,)
    def get_queryset(self):
        queryset = Article.objects.filter().order_by('-like')
        return queryset


########################## VOTE ARTICLE AND EXPRESS LIKE OR DISLIKE COMMENT ############################

class VoteArticleView(generics.CreateAPIView):
    queryset = VoteArticle.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VoteArticleSerializers
    def get_queryset(self): 
        query = VoteArticle.objects.filter(user=self.request.user)
        return query
    def perform_create(self, serializer):
        print(self.request)
        # tăng 1 lượt vote trên bài viết 
        articlecm = Article.objects.get(id = int(self.request.data["article"]))
        articlecm.like = articlecm.like + 1
        articlecm.save()
        serializer.save(user=self.request.user)

class DeleteVoteArticle(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = VoteArticleSerializers
    
    def get_queryset(self): 
        # giảm 1 lượt vote trên 1 bài viết 
        print(int(self.kwargs.get('pk')))
        vote = VoteArticle.objects.get(id = int(self.kwargs.get('pk')))
        articlecm = vote.article
        articlecm.like = articlecm.like - 1
        articlecm.save()
        query = VoteArticle.objects.filter(user=self.request.user)
        return query


class VoteComment(generics.CreateAPIView):
    queryset = LikeDislikeComment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ExpressCommentSerializers
    def get_queryset(self): 
        query = LikeDislikeComment.objects.filter(user=self.request.user)
        return query
    def perform_create(self, serializer):
        print(self.request)
        # tăng 1 lượt vote trên 1 comment 
        cmt = Comment.objects.get(id = int(self.request.data["comment"]))
        cmt.like = cmt.like + 1
        cmt.save()
        serializer.save(user=self.request.user)

class DeleteVoteComment(generics.DestroyAPIView): #Cập nhật bài đăng api/motels/update/<pk>
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ExpressCommentSerializers
    def get_queryset(self): #Authentication user để update
        # giảm 1 lượt vote trên 1 comment 
        votecmt = LikeDislikeComment.objects.get(id = int(self.kwargs.get('pk')))
        cmt = votecmt.comment
        cmt.like = cmt.like - 1
        cmt.save()
        query = LikeDislikeComment.objects.filter(user=self.request.user)
        return query

##################################################################################
class UserUnfollowAnimal (generics.DestroyAPIView): # User unfollow 1 animal's class
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagAnimalFollowSerializers
    queryset = UserFollowAnimal.objects.all()
    # def get_queryset(self): 
    #     query = UserFollowAnimal.objects.filter(user=self.request.user)
    #     return query
######################## FOLLOW AND UNFOLLOW A CLASS ###################################
class GetAllTagFollow (generics.RetrieveAPIView):  # lấy các tag animal mà user follow 
    permission_classes = (AllowAny,) 
    queryset = User.objects.all()
    serializer_class = UserFollowAnimalSerializers


class UserFollowAnimal(generics.CreateAPIView):  # User follow 1 animal's class
    queryset = UserFollowAnimal.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TagAnimalFollowSerializers
    def get_queryset(self): 
        query = UserFollowAnimal.objects.filter(user=self.request.user)
        return query
    def perform_create(self, serializer):
        print(self.request)
        serializer.save(user=self.request.user)


    
