from django.urls import path

from posts.api.views import ListCreatePostView

urlpatterns = [
    path('posts', ListCreatePostView.as_view(), name='posts'),
]