from django.urls import include, path
from .views import ActivateCreateToken
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, GenreViewSet


router = SimpleRouter()
router.register('authen', ActivateCreateToken)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
