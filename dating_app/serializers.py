from rest_framework import serializers

from rest_framework import serializers
from django.contrib.auth.models import User

from dating_app.models import Profile
from django.db.models import  Q


from rest_framework.serializers import (
    CharField,
    EmailField,
    
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )


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
class RegisterSerializer(serializers.HyperlinkedModelSerializer):
    profile = CustomProfileRegister(required=True)
    
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username', 'email', 'password','profile',)
        extra_kwargs = {'password': {'write_only': True},
                        }


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
    
    
    
# ---------------------------


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField()
    # email = serializers.EmailField(label='Email Address')
    
    class Meta:
        model = User
        fields = [
            'username',
            # 'email',
            'password',
            'token',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
        
    # #validate for incorrect details
    def validate(self, data):#data is built in dict
        user_obj=None
        # email = data.get('email',None)#if no email then None
        username = data.get('username',None)
        password = data.get('password')
        
        if not username:
            raise ValidationError("A username and email is required to login")
        
        user = User.objects.filter(
                                   Q(username=username)).distinct()
        
        
        
        user = user.exclude(username__iexact='')#it excludes null email and give relevant output
        print(user)
        if user.exists() and user.count() == 1:
            
            user_obj = user.first()#only one user obj so we set first
        else:
            raise ValidationError("The username is not valid")
            
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again")
        #otherwise
        data['token'] = "random token"
        
        user_qs = User.objects.filter(username=username)
        
        if user_qs.exists():
            raise ValidationError("This user has already login.")
        return data
    

class DetailSerializer(serializers.HyperlinkedModelSerializer):
    url = detail_url = HyperlinkedIdentityField(
        view_name='chat:detail-user',#where to go
        # lookup_field = 'slug'##id is default but here we use slug
    )
    class Meta:
        model = User
        fields = '__all__'
