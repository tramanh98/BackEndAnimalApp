from rest_framework import serializers
from .models import Article, Comment, ClassAnimal, VoteArticle, LikeDislikeComment, UserFollowAnimal
from user.models import User
import datetime
from user.serializers import  UserSerializer

class ArticleSerializer(serializers.ModelSerializer):  # create, update, get, delete bài đăng 
    id = serializers.IntegerField(source='pk', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('view', 'like', 'comment', 'created_at', 'updated_at')

class CommentSerializers (serializers.ModelSerializer):   # create, update, delete 1 comment
    id = serializers.IntegerField(source='pk', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('like', 'created_at', 'updated_at')

class VoteArticleSerializers (serializers.ModelSerializer):  # create, delete 1 vote
    id = serializers.IntegerField(source='pk', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = VoteArticle
        fields = '__all__'

class ExpressCommentSerializers (serializers.ModelSerializer):  # create, delete (like, dislike) expressing about 1 comment
    id = serializers.IntegerField(source='pk', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = LikeDislikeComment
        fields = '__all__'


################## Cooperate Serializers to get Detail Article with all comments and its vote #####################

class LDLCommentSerializers(serializers.ModelSerializer): # cooperate with CommentsWithVotesSerializers
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = LikeDislikeComment
        fields = ('id','user','vote')

class CommentsWithVotesSerializers(serializers.ModelSerializer): # cooperate with 
    id = serializers.IntegerField(source='pk', read_only=True)
    user = UserSerializer(read_only=True)
    votes = LDLCommentSerializers(many=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'article', 'content', 'like', 'votes', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class VotesWithArticleSerializer (serializers.ModelSerializer): 
    id = serializers.IntegerField(source='pk', read_only=True)  
    class Meta:
        model = VoteArticle
        fields = ('id', 'user', 'vote')

class GetDetailArticleSerializer (serializers.ModelSerializer): 
    id = serializers.IntegerField(source='pk', read_only=True)
    user = UserSerializer(read_only=True)
    votes = VotesWithArticleSerializer(many=True)
    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'content', 'typeClass', 'dangerous', 'underwater',
                  'terrestrial', 'pets', 'wild', 'rare', 'view','like','comment', 'created_at', 'updated_at',
                  'votes')
        read_only_fields = ('created_at', 'updated_at')

###############################################################################################

#################### Get user's articles and user's information  ########################

class GetAllArticleSerializer(serializers.ModelSerializer):  
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class UserArticleSerializers(serializers.ModelSerializer): 
    id = serializers.IntegerField(source='pk', read_only=True) 
    # articles = GetArticleSerializer(many=True)
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username', 'email', 'avatar', 'posts')


######################## Get Class's Article #######################

class AnimalArticleSerializers(serializers.ModelSerializer): 
    id = serializers.IntegerField(source='pk', read_only=True)
    articles = GetAllArticleSerializer(many=True)
    class Meta:
        model = ClassAnimal
        fields = ('id','name','articles') 

###########################################################################
####################### USER FOLLOW ANIMAL'S CLASS ########################

class TagAnimalFollowSerializers(serializers.ModelSerializer):  # follow and unfollow 1 class
    id = serializers.IntegerField(source='pk', read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserFollowAnimal
        fields = '__all__'


class UserTagSerializers(serializers.ModelSerializer): # kết hợp với UserFollowAnimalSerializers
    id = serializers.IntegerField(source='pk', read_only=True)
    class Meta:
        model = UserFollowAnimal
        fields = ('id','animal')

class UserFollowAnimalSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True) 
    followingtag = UserTagSerializers(many=True)
    class Meta:
        model = User
        fields = ('id','username','followingtag')




