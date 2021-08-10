from django.urls import path, include, re_path
from .views import ActivateCreateToken
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register('authen', ActivateCreateToken)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt')),
    path('v1/', include(router.urls)),
]
