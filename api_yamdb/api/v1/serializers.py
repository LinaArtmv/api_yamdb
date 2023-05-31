from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализация модели User."""

    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.RegexField(required=True,
                                      max_length=150,
                                      regex=r'^[\w.@+-]+$')

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        """Запрещает пользователям присваивать себе имя me
        и использовать повторные username и email."""

        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )

        if not User.objects.filter(username=data.get('username'),
                                   email=data.get('email')):
            if User.objects.filter(email=data.get('email')):
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует'
                )
            if User.objects.filter(username=data.get('username')):
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует'
                )
        return data


class UserTokenSerializer(serializers.Serializer):
    """Сериализация данных для получения токена."""

    username = serializers.RegexField(max_length=150,
                                      required=True,
                                      regex=r'^[\w.@+-]+$')
    confirmation_code = serializers.CharField(max_length=150, required=True)


class UserMeSerializer(UserSerializer):
    """Сериализация данных для эндпоинта users/me/."""

    role = serializers.ChoiceField(choices=['user', 'moderator', 'admin'],
                                   default='user')
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализация модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализация модели Title для чтения"""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        score_result = obj.reviews.aggregate(Avg('score'))
        rating = score_result['score__avg']
        return rating


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализация модели Title для создания или изменения объекта"""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация модели Review."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение!'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'author', 'text',
                  'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text',
                  'pub_date')
