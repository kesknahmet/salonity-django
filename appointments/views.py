from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Appointment, AppointmentReview
from .serializers import (
    AppointmentCreateSerializer, AppointmentListSerializer, 
    AppointmentDetailSerializer, AppointmentUpdateSerializer, AppointmentReviewSerializer
)

class AppointmentCreateView(generics.CreateAPIView):
    """Randevu oluşturma"""
    serializer_class = AppointmentCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Müşteri profilini otomatik olarak ekle
        customer = self.request.user.customer_profile
        
        # Fiyatı hizmet fiyatından al
        service = serializer.validated_data['service']
        price = service.price
        
        appointment = serializer.save(customer=customer, price=price)

class AppointmentListView(generics.ListAPIView):
    """Kullanıcının randevularını listele"""
    serializer_class = AppointmentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Appointment.objects.filter(customer__user=self.request.user).order_by('-appointment_date', '-appointment_time')

class AppointmentDetailView(generics.RetrieveAPIView):
    """Randevu detayları"""
    serializer_class = AppointmentDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Appointment.objects.filter(customer__user=self.request.user)

class AppointmentUpdateView(generics.UpdateAPIView):
    """Randevu güncelleme (sadece durum ve notlar)"""
    serializer_class = AppointmentUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Appointment.objects.filter(customer__user=self.request.user)

class AppointmentCancelView(generics.UpdateAPIView):
    """Randevu iptal etme"""
    serializer_class = AppointmentUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        return Appointment.objects.filter(customer__user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()
        return Response({'message': 'Randevu iptal edildi'}, status=status.HTTP_200_OK)

class AppointmentReviewCreateView(generics.CreateAPIView):
    """Randevu değerlendirmesi oluşturma"""
    serializer_class = AppointmentReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        appointment_id = self.kwargs.get('appointment_id')
        appointment = Appointment.objects.get(id=appointment_id, customer__user=self.request.user)
        serializer.save(
            appointment=appointment,
            customer=self.request.user.customer_profile,
            salon=appointment.salon
        )
