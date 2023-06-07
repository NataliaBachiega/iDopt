from django.urls import path

from posts.api.views import ListCreatePostView, RetrieveDeletePostView, ListCommentsView

urlpatterns = [
    path('posts/', ListCreatePostView.as_view(), name='posts'),
    path('posts/<int:pk>/', RetrieveDeletePostView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments/', ListCommentsView.as_view(), name='post-comments'),
]