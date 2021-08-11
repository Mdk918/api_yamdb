from django.urls import path, include
from .views import (ActivateCreateToken,
                    CreateUser,
                    CategoryViewSet,
                    GenreViewSet,
                    TitleViewSet,
                    ReviewViewSet,
                    CommentViewSet,)
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register('authen', ActivateCreateToken)
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
    path('v1/auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', CreateUser.as_view()),
    path('v1/', include(router.urls)),
]
