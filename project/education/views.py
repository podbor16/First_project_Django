from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

from education.serializers import *
from education.models import *


class SchoolViewset(viewsets.ModelViewSet):
    queryset = School.objects.all().filter(is_active=True)
    serializer_class = SchoolSerializer

    def destroy(self, request, format=None):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SClassViewset(viewsets.ModelViewSet):
    queryset = SClass.objects.all()
    serializer_class = SClassSerializer


class StudentViewest(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer