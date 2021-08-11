from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.dispatch import Signal
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework import filters, mixins, permissions, serializers, status, viewsets
from rest_framework.permissions import AllowAny


from reviews.models import User, Category, Genre, Title, Review, Comment
from .permissions import AdminOrReadOnly, AuthorOrModeratorOrAdminOrReadOnly
from .serializers import (UserCreateCustomSerializer,
                          CustomActivationSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          Title_GET_Serializer,
                          Title_OTHER_Serializer,
                          ReviewSerializer,
                          CommentSerializer)

# New user has registered. Args: user, request.
user_registered = Signal()

# User has activated his or her account. Args: user, request.
user_activated = Signal()


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateCustomSerializer
    permission_classes = (AllowAny,)


class ActivateToken(CreateAPIView):
    serializer_class = CustomActivationSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    token_generator = default_token_generator

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        user_activated.send(
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


class ReviewViewSet(viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(title=title, review=review, author=self.request.user)
