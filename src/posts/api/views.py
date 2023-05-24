from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from posts.api.serializers import PostSerializer

from posts.models import Post

class ListCreatePostView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)