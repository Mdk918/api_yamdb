from django.contrib.auth.tokens import default_token_generator
from django.dispatch import Signal
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import User, Category, Genre, Title, Review, Comment
from .filters import TitleFilter
from .permissions import (AdminOrReadOnly,
                          AuthorOrModeratorOrAdminOrReadOnly,
                          AdminOrSuperUser,
                          AdminOrAuthUser,
                          AdminOrSuperUserOrModerator)
from .serializers import (UserCreateCustomSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          Title_GET_Serializer,
                          Title_OTHER_Serializer,
                          ReviewSerializer,
                          CommentSerializer,
                          UserSerializers,
                          CustomUsernamedAndTokenSerializer)
from .filters import TitleFilter


# New user has registered. Args: user, request.
user_registered = Signal()

# User has activated his or her account. Args: user, request.
user_activated = Signal()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AdminOrSuperUser,)
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'me':
            return (AdminOrAuthUser(),)
        return super().get_permissions()

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        serializer = UserSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['get', 'patch', 'delete'], detail=False, url_name='me')
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'GET':
            if user.is_authenticated:
                serializer = self.get_serializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'PATCH':
            partial = kwargs.pop('partial', True)
            if user.is_authenticated:
                serializer = self.get_serializer(user, data=request.data, partial=partial)
                if serializer.is_valid():
                    if 'role' in request.data and request.user.role != 'admin':
                        role = request.data['role']
                        if role != request.user.role:
                            return Response(serializer.data)
                    self.perform_update(serializer)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'DELETE':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        if 'role' in request.data:
            role = request.data['role']
            if role not in ['admin', 'user', 'moderator']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateCustomSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


class ActivateToken(CreateAPIView):
    serializer_class = CustomUsernamedAndTokenSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    token_generator = default_token_generator

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)
        if user.is_active is True:
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(token, status=status.HTTP_200_OK)
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
        return Response(token, status=status.HTTP_200_OK)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AdminOrReadOnly, ]
        else:
            self.permission_classes = [AdminOrSuperUser, ]
        return super(CategoryViewSet, self).get_permissions()


class GenreViewSet(CreateListDestroyViewSet):
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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AdminOrReadOnly, ]
        else:
            self.permission_classes = [AdminOrSuperUser, ]
        return super(GenreViewSet, self).get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Title
    GenreViewSet реализует операции:
        <POST> - добавление нового тайтла, достпуно только Администратору
        <GET> - получение списка тайтлов, доступно без токена
        <GET + {title id}> - получение информации о тайтле, доступно без токена
        <DELETE> - удаление категории, доступно только Администратору
    Реализована фильтрация по полям: 'category', 'genre', 'name', 'year'
    """
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return Title_GET_Serializer
        return Title_OTHER_Serializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AdminOrReadOnly, ]
        else:
            self.permission_classes = [AdminOrSuperUser, ]
        return super(TitleViewSet, self).get_permissions()


class ReviewViewSet(viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination

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
    pagination_class = PageNumberPagination

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