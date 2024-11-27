# auth_flow/serializers.py

# from django.contrib.auth.models import User
from auth_flow.models import AllUsers as User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .permissions import IsAdminUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Validates unique email, matching passwords, and required fields.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]  # Ensure email is unique
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]  # Enforce strong password
    )
    password2 = serializers.CharField(write_only=True, required=True)  # Confirm password field

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name' , 'phone')

    def validate(self, attrs):
        # Check if the two passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Create the user with the provided data
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        # Check if the two new passwords match
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "New passwords didn't match."})
        return attrs


class GetUserSerializer(serializers.ModelSerializer):
    """
    Serializer for getting user details.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role','first_name', 'last_name', 'phone')


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user details.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone')

class RoleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the role of a user.
    Ensures the role is one of the valid choices.
    """

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('User', 'User')
    ]

    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['role']  # Only allow the role field to be updated

    def validate_role(self, value):
        """
        You can add any additional validation for the role here if needed.
        """
        return value