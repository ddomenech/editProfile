from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status, viewsets, mixins
from rest_framework.parsers import FileUploadParser
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserProfileSerializer, UserSerializer, PasswordSerializer, AvatarSerializer
from .models import User, UserProfile
from rest_framework.request import Request

from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsSameUserAllowEditionOrReadOnly, IsAdminUserOrReadOnly

# Create your views here.

class UserProfileViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    
    queryset=UserProfile.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,)

    @action(detail=True,methods=['put','patch'], serializer_class=PasswordSerializer)
    def set_password(self, request, pk):
        serializer =  PasswordSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({"status":"password set"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ''' @action(detail=True,methods=['put','patch'], serializer_class=AvatarSerializer)
    def change_avatar(self, request, pk, filename, format=None):
        parser_classes = (FileUploadParser,)
        permission_classes = (IsOwnerOrReadOnly,permissions.IsAuthenticated)
        
        file_obj = request.FILES
        if 'file' not in request.data:
            raise ParseError("Empty content")
        try:
            profile = UserProfile(user=request.user)
            profile.save(request.user, file_obj['file'])
        except Exception as e:
            raise e
        return Response(status=status.HTTP_201_CREATED) '''


class UserViewSet(viewsets.ModelViewSet):
    
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                            IsSameUserAllowEditionOrReadOnly,)
    

   
