from rest_framework import serializers

from posts.models import Post, Comment
from profiles.api.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    
    author = UserSerializer(required=False)

class CommentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Comment
        fields = '__all__'

    answer_of = serializers.PrimaryKeyRelatedField(
        queryset = Comment.objects.all(),
        required = False,
        allow_null = True,
    )