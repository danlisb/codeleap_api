from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "username", "created_datetime", "title", "content"]
        read_only_fields = ["id", "created_datetime"]


class PostUpdateSerializer(serializers.ModelSerializer):
    """Used for PATCH – only title and content are writable, but returns full object."""

    class Meta:
        model = Post
        fields = ["id", "username", "created_datetime", "title", "content"]
        read_only_fields = ["id", "username", "created_datetime"]
