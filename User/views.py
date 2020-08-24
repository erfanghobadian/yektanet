from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from .serializers import PersonSerializer, CompanySerializer, UserSerializer
from .models import User, CompanyProfile, PersonProfile
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class SignUpPersonView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PersonSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            # response_data = {}
            # response_data.update(serializer.data)
            # response_data['user']['token'] = serializer.token
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class SignUpCompanyView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CompanySerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            # response_data = {}
            # response_data.update(serializer.data)
            # response_data['user']['token'] = serializer.token
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class EditProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    def get_object(self):
        if self.request.user.user_type == 1:
            return self.request.user.companyprofile
        elif self.request.user.user_type == 2:
            return self.request.user.personprofile

    def get_serializer_class(self):
        if self.request.user.user_type == 1:
            return CompanySerializer
        elif self.request.user.user_type == 2:
            return PersonSerializer
