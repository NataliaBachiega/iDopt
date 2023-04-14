from django.urls import path

from profiles.api.views import VerifyEmail

urlpatterns = [
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
]