from djoser.views import UserViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from djoser import signals
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, serializers, status, viewsets
from reviews.models import Category, Genre, Title
from .permissions import AdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, Title_GET_Serializer, Title_OTHER_Serializer


class ActivateCreateToken(UserViewSet):
    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )
        refresh = RefreshToken.for_user(user)

        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(token, status=status.HTTP_204_NO_CONTENT)



class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Вьюесет модели Category
    CategoryViewSet реализует операции:
        <POST> - добавление новой категории, достпуно только Администратору
        <GET> - получение списка категорий, доступно без токена
        <DELETE> - удаление категории, доступно только Администратору
    Есть поиск по полю 'name'
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    """
    Вьюесет модели Genre
    GenreViewSet реализует операции:
        <POST> - добавление новой категории, достпуно только Администратору
        <GET> - получение списка категорий, доступно без токена
        <DELETE> - удаление категории, доступно только Администратору
    Есть поиск по полю 'name'
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Title
    GenreViewSet реализует операции:
        <POST> - добавление нового произведения, достпуно только Администратору
        <GET> - получение списка произведений, доступно без токена
        <GET + {title id}> - получение информации о произведении, доступно без токена
        <DELETE> - удаление категории, доступно только Администратору
    Реализована фильтрация по полям: 'category', 'genre', 'name', 'year'
    """
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == "GET":
            return Title_GET_Serializer
        return Title_OTHER_Serializer
