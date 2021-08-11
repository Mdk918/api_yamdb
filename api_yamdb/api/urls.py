from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import ActivateCreateToken,CategoryViewSet, GenreViewSet, TitleViewSet


router = SimpleRouter()
router.register('authen', ActivateCreateToken)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
