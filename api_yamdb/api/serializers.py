from rest_framework import serializers
from reviews.models import Category, Genre, Title

from users.models import CustomUser


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'first_name', 'last_name',
            'username', 'bio',
            'email', 'role',
        )
        model = CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
