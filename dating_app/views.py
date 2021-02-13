from django.shortcuts import render, get_object_or_404


# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, CustomProfileRegister, UserLoginSerializer, DetailSerializer
from django.shortcuts import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# from rest_framework.authentication import CsrfExemptSessionAuthentication, BasicAuthentication 
from braces.views import CsrfExemptMixin

# from dating_app.models import Profile

# Register API
class Register(generics.GenericAPIView):
    serializer_class =   RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       

@api_view(['GET'])
def ListUserDetail(request):
    serializer = User.objects.all()
    user_data = RegisterSerializer(serializer, many = True)
    return Response(user_data.data)

@api_view(['GET'])
def DetailUser(request, pk):
    serializer = get_object_or_404(User,id = pk)
    user_data = RegisterSerializer(serializer, many = False)
    return Response(user_data.data)
    
        
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication
from django.views.decorators.csrf import csrf_exempt


# class Login(CsrfExemptMixin, KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = [BasicAuthentication]
#     # serializer_class = UserLoginSerializer
 
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return HttpResponse(user)
#         return super(Login, self).post(request, format=None)
    
    
    
class Login(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        
        #if invalid
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


## To change password
from rest_framework import status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
       
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)