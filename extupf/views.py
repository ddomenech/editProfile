from rest_framework import status, viewsets, mixins
from rest_framework import permissions
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserProfile
from .permissions import IsOwnerOrReadOnly, IsSameUserAllowEditionOrReadOnly, \
    IsOwner
from .serializers import UserProfileSerializer, UserSerializer, \
    PasswordSerializer


class UserProfileViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user_id=user.id)

    @action(detail=True, methods=['put', 'patch'], serializer_class=PasswordSerializer)
    def set_password(self, request, pk):
        serializer = PasswordSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({"status": "password set"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user_id=self.request.user.id)
        return self.queryset
