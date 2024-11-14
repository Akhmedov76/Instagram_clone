from rest_framework import serializers

from app_post.models import *


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['user', 'text', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = ['user']

    def validate(self, data):
        if data['user'] == self.context['request'].user:
            raise serializers.ValidationError('You can not like your own comment')
        return data


class PostSerializers(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostModel
        fields = ['id', 'title', 'image', 'caption', 'created_at', 'updated_at', 'user', 'comments']
        read_only_fields = ['created_at', 'updated_at', 'user']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['title', 'image', 'caption']

    def create(self, validated_data):
        author = validated_data.pop('author')
        post = PostModel.objects.create(author=author, **validated_data)
        return post
