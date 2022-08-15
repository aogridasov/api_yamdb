from rest_framework import serializers
from users.models import User

from reviews.models import Category, Comment, Genres, Review, Titles


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Titles
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'score', 'title', 'author', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date',)
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        """
        Валидация username
        """
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Нельзя создавать юзера с ником me"
            )
        return value

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=32,
    )
    username = serializers.CharField(max_length=200)


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role',)


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)
