from django.urls import path

from profiles.api.views import Registration, VerifyEmail

urlpatterns = [
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('register/', Registration.as_view(), name='register'),
]