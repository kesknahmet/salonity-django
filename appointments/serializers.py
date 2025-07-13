from rest_framework import serializers
from .models import Appointment, AppointmentReview
from salons.models import Salon, SalonEmployee
from services.models import Service
from customers.models import Customer

class AppointmentCreateSerializer(serializers.ModelSerializer):
    """Randevu oluşturma için"""
    class Meta:
        model = Appointment
        fields = ['salon', 'service', 'employee', 'appointment_date', 'appointment_time', 'notes', 'customer_notes']
    
    def validate(self, data):
        # Randevu tarihinin geçmiş olmaması kontrolü
        from datetime import date
        if data['appointment_date'] < date.today():
            raise serializers.ValidationError("Geçmiş tarih için randevu oluşturulamaz.")
        
        # Çalışanın o hizmeti verebilip veremediği kontrolü
        if data.get('employee'):
            service = data['service']
            employee = data['employee']
            if not service.employees.filter(employee=employee, is_available=True).exists():
                raise serializers.ValidationError("Seçilen çalışan bu hizmeti veremez.")
        
        return data

class AppointmentListSerializer(serializers.ModelSerializer):
    """Randevu listesi için"""
    salon_name = serializers.CharField(source='salon.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'salon_name', 'service_name', 'employee_name', 'appointment_date', 
                 'appointment_time', 'end_time', 'status', 'status_display', 'price', 'created_at']

class AppointmentDetailSerializer(serializers.ModelSerializer):
    """Randevu detay bilgileri"""
    salon_name = serializers.CharField(source='salon.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'salon', 'salon_name', 'service', 'service_name', 'employee', 'employee_name',
                 'appointment_date', 'appointment_time', 'end_time', 'status', 'status_display',
                 'notes', 'customer_notes', 'price', 'created_at', 'updated_at', 'confirmed_at', 'completed_at']

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """Randevu güncelleme için"""
    class Meta:
        model = Appointment
        fields = ['status', 'notes', 'customer_notes']
        read_only_fields = ['customer', 'salon', 'service', 'employee', 'appointment_date', 'appointment_time']

class AppointmentReviewSerializer(serializers.ModelSerializer):
    """Randevu değerlendirmesi"""
    customer_name = serializers.CharField(source='customer.user.username', read_only=True)
    
    class Meta:
        model = AppointmentReview
        fields = ['id', 'rating', 'comment', 'salon_response', 'customer_name', 'created_at']
        read_only_fields = ['appointment', 'customer', 'salon'] 