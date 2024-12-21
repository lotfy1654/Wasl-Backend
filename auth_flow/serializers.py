# auth_flow/serializers.py

# from django.contrib.auth.models import User
from auth_flow.models import AllUsers as User , Employee , PasswordResetOTP
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
# from django.core.mail import send_mail
# from datetime import datetime, timedelta
# import random


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
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name' , 'phone','profile_picture' , 'country' , 'date_of_birth')

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
            phone=validated_data['phone'],
            profile_picture=validated_data['profile_picture'],
            country=validated_data['country'],
            date_of_birth=validated_data['date_of_birth']
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
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'phone', 'profile_picture' , 'country' , 'date_of_birth')

    def get_profile_picture(self, obj):
        request = self.context.get('request')  # Get the request object
        if obj.profile_picture:  # Only build the URL if profile_picture is not None
            return request.build_absolute_uri(obj.profile_picture.url) if request else obj.profile_picture.url
        return None


class GetAllPersonInSystemSerializers(serializers.ModelSerializer):
    """
    Serializer for listing all users in the system.
    This directly serializes the User model fields.
    """
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'phone', 'profile_picture', 'country', 'date_of_birth')

    def get_profile_picture(self, obj):
        request = self.context.get('request')  # Get the request object
        if obj.profile_picture:
            return request.build_absolute_uri(obj.profile_picture.url)  # Construct the absolute URL
        return None



class UpdateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user details.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone' , 'profile_picture' , 'country' , 'date_of_birth')

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
    

class EmployeeSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()
    class Meta:
        model = Employee
        fields = '__all__'

class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeNameIdSerializer(serializers.ModelSerializer):
    
    user = GetUserSerializer()
    
    class Meta:
        model = Employee
        fields = ['id', 'user']




# Forget Password Serializers
# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate_email(self, value):
#         try:
#             self.user = User.objects.get(email=value)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User with this email does not exist.")
#         return value

#     def save(self):
#         otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
#         expiry_time = datetime.now() + timedelta(minutes=10)  # OTP valid for 10 minutes

#         # Create OTP entry
#         PasswordResetOTP.objects.create(
#             user=self.user,
#             otp=otp,
#             expiry_time=expiry_time
#         )

#         # Send OTP via email or other communication method
#         self.send_otp_email(self.user.email, otp)

#     def send_otp_email(self, email, otp):
#         send_mail(
#             'Password Reset OTP',
#             f'Your OTP for password reset is: {otp}',
#             'from@example.com',  # Your sending email address
#             [email],  # Recipient email
#             fail_silently=False,
#         )


# class PasswordResetVerifySerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)

#     def validate(self, data):
#         try:
#             user = User.objects.get(email=data['email'])
#             otp_entry = PasswordResetOTP.objects.get(user=user, otp=data['otp'])

#             if otp_entry.is_expired():
#                 raise serializers.ValidationError("OTP has expired.")
#         except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
#             raise serializers.ValidationError("Invalid email or OTP.")

#         self.user = user
#         return data


# class PasswordResetSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)
#     new_password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         try:
#             user = User.objects.get(email=data['email'])
#             otp_entry = PasswordResetOTP.objects.get(user=user, otp=data['otp'])

#             if otp_entry.is_expired():
#                 raise serializers.ValidationError("OTP has expired.")
#         except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
#             raise serializers.ValidationError("Invalid email or OTP.")

#         self.user = user
#         return data

#     def save(self):
#         self.user.set_password(self.validated_data['new_password'])
#         self.user.save()
