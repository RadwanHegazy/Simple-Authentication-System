from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class RegisterSeriailzer (serializers.ModelSerializer)  :
    
    password = serializers.CharField(max_length=1000,min_length=5,write_only=True)

    class Meta:
        model = User
        fields = ('id','username','email','password')

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        user = User.objects.create_user(username=username, email=email, password = password)
        Token.objects.create(user=user)

        return user

class LoginSerializer (serializers.ModelSerializer) : 
    class Meta:
        model = User
        fields = ('email','password')

    def create(self, validated_data):

        return super().create(validated_data)


class ProfileSerializer (serializers.ModelSerializer) : 
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email')