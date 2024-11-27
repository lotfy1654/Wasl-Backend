# auth_flow/urls.py

from django.urls import path
from .views import RegisterView, LoginView, LogoutView , ChangePasswordView , GetUserData , UpdateUserData , UpdateUserRole

# Define URL patterns for authentication endpoints
urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),  # Registration endpoint
    path('login', LoginView.as_view(), name='login'),           # Login endpoint
    path('logout', LogoutView.as_view(), name='logout'),        # Logout endpoint
    path('change-password', ChangePasswordView.as_view(), name='change-password'),  # Change password endpoint
    path('get-user-data', GetUserData.as_view(), name='get-user-data'),  # Get user data endpoint
    path('update-user-data', UpdateUserData.as_view(), name='update-user-data'),  # Update user data endpoint
    path('role-update/<int:pk>', UpdateUserRole.as_view(), name='role-update'),  # Role update endpoint
]
