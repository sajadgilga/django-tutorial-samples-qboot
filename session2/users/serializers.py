from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Book, Comment


class BookLeanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_null=False, min_length=3)


def validate_no_space(value: str):
    if ' ' in value:
        raise serializers.ValidationError('no space is allowed')
    return value


class SeparatorConvertorField(serializers.Field):
    def to_representation(self, field):
        return field.replace('--', ' ')

    def to_internal_value(self, data):
        return data.replace(' ', '--')


class CustomNameField(serializers.CharField):
    def to_representation(self, value):
        data = super().to_representation(value)
        return data[6:]

    def to_internal_value(self, data):
        data = f'name: {data}'
        return super().to_internal_value(data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['books', 'username', 'id', 'password', 'name']
        read_only_fields = ['username']
        depth = 0
        extra_kwargs = {'password': {'write_only': True}}

    def get_name(self, obj: User):
        request = self.context.get('request')
        return f'{request.user}::{obj.first_name} {obj.last_name}'


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = SeparatorConvertorField(allow_null=True)
    name = CustomNameField(allow_null=False, min_length=3, validators=[])
    author = serializers.CharField(allow_null=True, allow_blank=True, validators=[])
    active = serializers.BooleanField(source='is_active', read_only=True)
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-profile', lookup_url_kwarg='user_id')

    # def validate_name(self, value):
    #     print(f'name value: {value}')
    #     if Book.objects.filter(name=value).exists():
    #         raise serializers.ValidationError("Book name must be unique")
    #     return value

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text')
        instance.name = validated_data.get("name")
        instance.author = validated_data.get('author')
        instance.save()
        return instance

    def create(self, validated_data):
        instance = Book.objects.create(**validated_data)
        return instance

    class Meta:
        validators = [
            # UniqueTogetherValidator(
            #     Book.objects.all(),
            #     ['author', 'name']
            # )
        ]


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()
    book = BookSerializer()

    def create(self, validated_data):
        book_data = validated_data.pop('book')
        try:
            book = Book.objects.get(**book_data)
        except Book.DoesNotExist:
            book = Book.objects.create(**book_data)
        return Comment.objects.create(**validated_data, book=book)
