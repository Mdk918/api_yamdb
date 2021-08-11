from django.urls import path, include
from .views import (
                    CreateUser,
                    CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet,
                    ActivateToken)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+/comments)',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', CreateUser.as_view()),
    path('v1/auth/token/', ActivateToken.as_view()),
    path('v1/', include(router.urls)),
]
