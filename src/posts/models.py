from datetime import datetime
from django.db import models

from profiles.models import IdoptUser

class Post(models.Model):
    author: IdoptUser = models.ForeignKey(
        IdoptUser, on_delete=models.CASCADE, related_name='posts'
    )
    
    content: str = models.TextField()
    
    created_at: datetime = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    content: str = models.TextField()
    author: IdoptUser = models.ForeignKey(
        IdoptUser, on_delete=models.CASCADE, related_name='comments'
    )
    comment_of: Post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    answer_of = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='answers'
    ) 