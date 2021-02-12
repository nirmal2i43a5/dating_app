from rest_framework import serializers

from rest_framework import serializers
from django.contrib.auth.models import User

from dating_app.models import Profile

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CustomProfileRegister(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone','dob','gender','looking_for','avatar')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    profile = CustomProfileRegister(required=True)
    
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username', 'email', 'password','profile',)
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],email=validated_data['email'],
                                        password=validated_data['password'])

    
        profile_data = validated_data.pop('profile')
        # create profile
        profile = Profile.objects.create(
            user = user,
            phone = profile_data['phone'],
            dob = profile_data['dob'],
             gender = profile_data['gender'],
              looking_for = profile_data['looking_for'],
              avatar = profile_data['avatar'],
            # etc...
        )
        
        
        return user




class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)