from rest_framework import serializers
from django.contrib.auth import get_user_model,  authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture']
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(   
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None),
        )
        Token.objects.create(user=user)    
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()   
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        token, created = Token.objects.get_or_create(user=user)
        return {
            "user": user,
            "token": token.key
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class SimpleUserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)


    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'followers_count', 'following_count')
