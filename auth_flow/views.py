# auth_flow/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer , ChangePasswordSerializer ,GetUserSerializer , UpdateUserSerializer , RoleUpdateSerializer 
from .models import AllUsers as User    


class RegisterView(APIView):
    """
    View for user registration.
    Allows any user to register with a POST request.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new user
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.
    Authenticates a user and returns JWT tokens upon successful authentication.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                # Extract username and password from the serializer
                username = serializer.data['username']
                password = serializer.data['password']
                
                # Check if the input is an email or username
                user = None
                if '@' in username:
                    # If it contains '@', it's likely an email, so try fetching user by email
                    try:
                        user = User.objects.get(email=username)
                    except User.DoesNotExist:
                        user = None
                else:
                    # Otherwise, treat it as a username
                    try:
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        user = None

                # Authenticate the user
                if user is not None and user.check_password(password):
                    # Generate tokens if authentication is successful
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'role': user.role,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    })
                else:
                    # Invalid credentials
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # Validation error
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class LogoutView(APIView):
    """
    Logout the user by blacklisting the refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request body (not from Authorization header)
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the token to prevent further use
            except Exception as e:
                return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ChangePasswordView(APIView):
    """
    API endpoint for changing user password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                # Extract old and new passwords from the serializer
                old_password = serializer.data['old_password']
                new_password = serializer.data['new_password']
                
                # Check if the old password is correct
                if not request.user.check_password(old_password):
                    return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
                
                # Change the password
                request.user.set_password(new_password)
                request.user.save()
                
                return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetUserData(APIView):
    """
    API endpoint for getting user details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = GetUserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class UpdateUserData(APIView):
    """
    API endpoint for updating user details.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Check if the request body is empty
            if not request.data:
                return Response({"message": "No data provided to update"}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize the request data with partial updates
            serializer = UpdateUserSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User details updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UpdateUserRole(APIView):
    """
    Class-based view to update user roles. Only accessible to admin users.
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if request.user.role != 'Admin':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        else:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the admin is trying to update their own role
            if user == request.user:
                return Response({"detail": "You cannot change your own role."}, status=status.HTTP_400_BAD_REQUEST)

            # Use the RoleUpdateSerializer to validate and update the user role
            serializer = RoleUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                # Save the updated user role
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)