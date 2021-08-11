from django.db import IntegrityError, transaction
from rest_framework import exceptions, serializers, status
from djoser.conf import settings
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from reviews.models import User, Category, Genre, Title, Review, Comment


class UserCreateCustomSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(style={"input_type": "email"}, write_only=True)

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
            user = User.objects.create_user(**validated_data)
            user.is_active = False
            user.save(update_fields=["is_active"])
            token = default_token_generator.make_token(user)
            send_mail('Тема письма',
                      f'Confirmation code {token}',
                      'from@example.com',  # Это поле "От кого"
                      [user.email],)
        return user


class CustomUsernamedAndTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    default_error_messages = {
        "invalid_token": "invalid token",
        "invalid_username": "invalid_username",
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        try:
            username = self.initial_data.get("username", "")
            self.user = User.objects.get(username=username)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_username"
            raise ValidationError(
                {"username": [self.error_messages[key_error]]}, code=key_error
            )

        is_token_valid = self.context["view"].token_generator.check_token(
            self.user, self.initial_data.get("confirmation_code", "")
        )
        if is_token_valid:
            return validated_data
        else:
            key_error = "invalid_confirmation_code"
            raise ValidationError(
                {"confirmation_code": [self.error_messages[key_error]]}, code=key_error
            )


class CustomActivationSerializer(CustomUsernamedAndTokenSerializer):
    default_error_messages = {
        "stale_token": "stale_token",
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_active:
            return attrs
        raise exceptions.PermissionDenied(self.error_messages["stale_token"])


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