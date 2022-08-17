from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'genre',
                  'category', 'description', 'rating')
        model = Title

    def get_rating(self, obj):
        avg_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        if avg_score:
            return round(avg_score)


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'category', 'genre', 'description', 'rating'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title = self.context['view'].kwargs['title_id']
        author = self.context['view'].request.user.id
        request_method = self.context['request'].method

        if Review.objects.filter(
            title=title, author=author
        ).exists() and request_method == 'POST':
            raise serializers.ValidationError(
                'Вы уже обозревали это произведение!'
            )
        return data

    def validate_score(self, value):
        if not (0 <= value <= 10):
            raise serializers.ValidationError('Оцените от 0 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date',)


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
