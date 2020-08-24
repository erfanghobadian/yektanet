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
from rest_framework import filters


class Node:
    def __init__(self, key, pk):
        self.left = None
        self.right = None
        self.val = key
        self.pk = pk


def sortedArrayToBST(arr):
    if not arr:
        return None

    mid = int((len(arr)) / 2)

    root = arr[mid]

    root.left = sortedArrayToBST(arr[:mid])
    root.right = sortedArrayToBST(arr[mid + 1:])
    return root


def RangeFilter(mn, mx, root):
    ans = []

    def rec(minr, maxr, rootr):
        if rootr is None:
            return
        if rootr.val < minr:
            rec(minr, maxr, rootr.right)
        if rootr.val > maxr:
            rec(minr, maxr, rootr.left)
        if minr <= rootr.val <= maxr:
            ans.append(rootr.pk)
            rec(minr, maxr, rootr.left)
            rec(minr, maxr, rootr.right)
        return

    rec(mn, mx, root)
    return ans


class SalaryRangeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_salary = request.query_params.get("min_salary", 0)
        max_salary = request.query_params.get("max_salary", 1000000000000000000)
        works = Work.objects.all()
        arr = []
        for work in works:
            node = Node(work.salary, work.pk)
            arr.append(node)
        arr = sorted(arr, key=lambda nd: nd.val)
        root = sortedArrayToBST(arr)
        pks = RangeFilter(int(min_salary), int(max_salary), root)
        qs = Work.objects.filter(pk__in=pks)
        return qs


class WorkList(generics.ListAPIView):
    def get_queryset(self):
        return Work.objects.all()

    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, SalaryRangeFilter]
    ordering_fields = ['expire_date', 'hours', 'salary']
    search_fields = ['title']


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
        if timezone.now() < work.expire_date:
            submit, created = WorkSubmit.objects.get_or_create(person=request.user.personprofile, work=work)
            submit.save()
            return Response("Your Application Added Successfully", status=status.HTTP_200_OK)
        return Response("Work expired", status=status.HTTP_400_BAD_REQUEST)


class ListApplications(generics.ListAPIView):
    permission_classes = [IsAuthenticated, user_permissions.IsCompany]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return WorkSubmit.objects.filter(work__company=self.request.user.companyprofile)
