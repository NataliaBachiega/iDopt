from django.urls import path

from posts.api.views import ListCreatePostView, RetrieveDeletePostView

urlpatterns = [
    path('posts/', ListCreatePostView.as_view(), name='posts'),
    path('posts/<int:pk>/', RetrieveDeletePostView.as_view(), name='post-detail')
]