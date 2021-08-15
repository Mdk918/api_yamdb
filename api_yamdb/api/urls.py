from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (ActivateToken,
                    CategoryViewSet,
                    CommentViewSet,
                    CreateUser,
                    GenreViewSet,
                    ReviewViewSet,
                    TitleViewSet,
                    UserViewSet,)

router = SimpleRouter()

auth = [
    path('signup/', CreateUser.as_view()),
    path('token/', ActivateToken.as_view()),
]

router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/auth/', include(auth)),
    path('v1/', include(router.urls)),
]
