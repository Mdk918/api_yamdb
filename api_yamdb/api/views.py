from djoser.views import UserViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from djoser import signals
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ActivateCreateToken(UserViewSet):
    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )
        refresh = RefreshToken.for_user(user)

        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(token, status=status.HTTP_204_NO_CONTENT)


