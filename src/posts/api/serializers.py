from rest_framework import serializers

from posts.models import Post
from profiles.api.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1
    
    author = UserSerializer(required=False)

    comment_of = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(), required=False
    )