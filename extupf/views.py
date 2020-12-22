from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .permissions import IsOwner
from .serializers import UserProfileSerializer, PasswordSerializer


class UserProfileViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwner, IsAuthenticated)
    parser_classes = (JSONParser, MultiPartParser, FileUploadParser)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)

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
