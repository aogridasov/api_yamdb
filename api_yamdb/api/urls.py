from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views as v


router = routers.DefaultRouter()
router.register(r'categories', v.CategoryViewSet, basename='categories')
router.register(r'genres', v.GenresViewSet, basename='genres')
router.register(r'titles', v.TitlesViewSet, basename='titles')
router.register(r'auth/signup', v.SignupViewSet, basename='signup')
router.register(r'auth/token', v.TokenViewSet, basename='gettoken')

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    v.ReviewViewSet,
    basename='reviews')

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    v.CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
