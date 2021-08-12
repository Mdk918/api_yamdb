from django.db import IntegrityError, transaction
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import random

from reviews.models import User, Category, Genre, Title, Review, Comment


class UserCreateCustomSerializer(serializers.ModelSerializer):

    default_error_messages = {
        "cannot_create_user": "cannot_create_user"
    }

    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            if validated_data['username'] == 'me':
                raise serializers.ValidationError(
                    'Использование данного имени запрещено'
                )
            user = User.objects.create_user(**validated_data)
            user.is_active = False
            user.save(update_fields=["is_active"])
            token = default_token_generator.make_token(user)
            send_mail('Тема письма',
                      f'Confirmation code {token}',
                      'from@yamdb.com',
                      [user.email],)
        return user


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class CustomUsernamedAndTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        username = self.initial_data.get("username", "")
        self.user = get_object_or_404(User, username=username)
        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("confirmation_code", "")
        )
        if is_token_valid:
            return validated_data
        else:
            raise ValidationError(
                "invalid_confirmation_code"
            )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class Title_GET_Serializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class Title_OTHER_Serializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


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
