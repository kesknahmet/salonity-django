from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ServiceCategory, Service
from salons.serializers import ServiceCategorySerializer, ServiceSerializer

# Create your views here.

class ServiceListView(generics.ListAPIView):
    """Tüm aktif hizmetleri listele"""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

class ServiceCategoryListView(generics.ListAPIView):
    """Hizmet kategorileri listesi"""
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [AllowAny]

class SalonServicesView(generics.ListAPIView):
    """Belirli bir salonun hizmetleri"""
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        salon_id = self.kwargs.get('salon_id')
        return Service.objects.filter(salon_id=salon_id, is_active=True)
