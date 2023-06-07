from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from posts.api.serializers import PostSerializer
from rest_framework.exceptions import PermissionDenied

from posts.models import Post
from rest_framework import mixins


class ListCreatePostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RetrieveDeletePostView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied(
                "Você não tem permissão para deletar este post.")
        super().perform_destroy(instance)

class ListCommentsView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        return Post.objects.filter(comment_of=post_id)
