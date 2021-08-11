from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers
from djoser.conf import settings
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title, User


class UserCreateCustomSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        style={"input_type": "email"}, write_only=True
    )

    default_error_messages = {
        "cannot_create_user": (
            settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
        )
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "email",
        )

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


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
        fields = ('name', 'year', 'description', 'category', 'genre')


class Title_OTHER_Serializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), many=True, slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre')
