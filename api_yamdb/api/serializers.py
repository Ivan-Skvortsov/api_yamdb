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


class SendEmailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25, required=True)

    def validate(self, data):
        username = data['username']
        if len(username) <= 2:
            raise serializers.ValidationError('Короткое имя польозвателя')
        return data

    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25, required=True)
    confirmation_code = serializers.CharField(required=True)


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


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitleWriteSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
