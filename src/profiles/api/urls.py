from django.urls import path

from profiles.api.views import LoginView, Registration, VerifyEmail

urlpatterns = [
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('register/', Registration.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]