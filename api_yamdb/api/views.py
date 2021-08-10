# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Genre, Review, Comment, Title

from .permissions import AuthorOrModeratorOrAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer


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
    permission_classes = ()
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
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
    permission_classes = ()
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


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
