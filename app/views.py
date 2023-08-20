from django.shortcuts import render
from .serializers import RegisterSeriailzer, ProfileSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status, mixins, decorators, permissions, authentication
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django.contrib.auth.views import auth_login
from rest_framework.authtoken.models import Token

@decorators.api_view(['GET',"PUT","DELETE"])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.TokenAuthentication])
def Profile (request) :
    user = request.user
    
    if request.method == "GET" :
        seriailzer = ProfileSerializer(user)
        return Response(seriailzer.data,status=status.HTTP_200_OK)
    
    if request.method == "PUT" : 
        seriailzer = ProfileSerializer(user, request.data)
        if seriailzer.is_valid() :
            seriailzer.save()
            return Response(seriailzer.data,status=status.HTTP_200_OK)
        return Response(seriailzer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE" : 
        user.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


@decorators.api_view(['POST'])
def login (request) :

    if request.method == "POST" : 
        email = request.POST['email']
        password = request.POST['password']

        print(email, password)

        user = User.objects.filter(email=email).first()

        if not user :
            raise ValidationError('User Not Found')
        
        if not user.check_password(password) :
            raise ValidationError('password error')
        
        user_seriailizer = ProfileSerializer(user).data
        user_seriailizer['token'] = Token.objects.get(user=user).key


        return Response(data=user_seriailizer,status=status.HTTP_200_OK)


    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserRegister (generics.GenericAPIView) :
    serializer_class = RegisterSeriailzer

    def post (self, request) : 
        seializer = self.serializer_class(data=request.data)

        if seializer.is_valid():
            seializer.save()
            data = seializer.data
            token = Token.objects.get(user=User.objects.get(id=data['id']))
            data['token'] = token.key
            return Response(data=data,status=status.HTTP_201_CREATED)
        else :
            return Response(seializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
            