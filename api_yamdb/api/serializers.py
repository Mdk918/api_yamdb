from rest_framework import serializers
from reviews.models import Category, Genre, Review, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('text', 'score')
        read_only_fields = ('title', 'author')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text',)
        read_only_fields = ('title', 'review', 'author')
