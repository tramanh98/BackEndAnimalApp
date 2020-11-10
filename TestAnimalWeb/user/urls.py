from django.conf.urls import url
from django.urls import path, include

from rest_framework import routers
from .views import ProfileUpdateDeleteAPIView, MyProfile, AvatarUpdateView

app_name = 'user'

router = routers.DefaultRouter()
router.register(r'update', ProfileUpdateDeleteAPIView, basename="Posts")

urlpatterns = [
    path('myprofile/', MyProfile.as_view()),
    path('avatar/update/', AvatarUpdateView.as_view()),  # update riêng avatar của user 
    # path('authenticate/', CustomObtainAuthToken.as_view()),
    # path('api/profile/', include(router.urls)),
]