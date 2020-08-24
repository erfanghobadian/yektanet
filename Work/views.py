from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from .models import Work, WorkSubmit
from .serializers import WorkSerializer, WorkSubmitSerializer, ApplicationSerializer
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from Work.permissions import IsOwner
from User import permissions as user_permissions
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta


class WorkList(generics.ListAPIView):
    def get_queryset(self):
        return Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]


class WorkDetail(generics.RetrieveAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]


class WorkDelete(generics.RetrieveDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class WorkUpdate(generics.RetrieveUpdateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class WorkCreate(generics.CreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated, user_permissions.IsCompany]

    def post(self, request, *args, **kwargs):
        serializer = WorkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


class SubmitWork(generics.CreateAPIView):
    queryset = WorkSubmit.objects.all()
    permission_classes = [IsAuthenticated, user_permissions.IsPerson]
    serializer_class = WorkSubmitSerializer

    def post(self, request, *args, **kwargs):
        work = Work.objects.get(pk=request.data['work'])
        if timezone.now() < work.expire_date :
            submit, created = WorkSubmit.objects.get_or_create(person=request.user.personprofile, work=work)
            submit.save()
            return Response("Your Application Added Successfully", status=status.HTTP_200_OK)
        return Response("Work expired", status=status.HTTP_400_BAD_REQUEST)


class ListApplications(generics.ListAPIView):
    permission_classes = [IsAuthenticated, user_permissions.IsCompany]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return WorkSubmit.objects.filter(work__company=self.request.user.companyprofile)
