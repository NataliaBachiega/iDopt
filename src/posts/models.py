from datetime import datetime
from django.db import models

from profiles.models import IdoptUser

class Post(models.Model):
    author: IdoptUser = models.ForeignKey(
        IdoptUser, on_delete=models.CASCADE, related_name='posts'
    )
    
    content: str = models.TextField()

    comment_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='comments')
    
    created_at: datetime = models.DateTimeField(auto_now_add=True)
