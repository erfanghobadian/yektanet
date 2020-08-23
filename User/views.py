from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import (AllowAny)
from .serializers import PersonSerializer, CompanySerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status


class SignUpPersonView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PersonSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)
