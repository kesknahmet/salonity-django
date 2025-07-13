from django.db import models
from django.contrib.auth.models import User
from salons.models import Salon, SalonEmployee
from services.models import Service
from customers.models import Customer
import uuid

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('confirmed', 'Onaylandı'),
        ('completed', 'Tamamlandı'),
        ('cancelled', 'İptal Edildi'),
        ('no_show', 'Gelmedi'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    employee = models.ForeignKey(SalonEmployee, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    
    # Randevu zamanı
    appointment_date = models.DateField(verbose_name='Randevu Tarihi')
    appointment_time = models.TimeField(verbose_name='Randevu Saati')
    end_time = models.TimeField(verbose_name='Bitiş Saati', null=True, blank=True)
    
    # Durum ve notlar
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Durum')
    notes = models.TextField(blank=True, verbose_name='Notlar')
    customer_notes = models.TextField(blank=True, verbose_name='Müşteri Notları')
    
    # Fiyat bilgisi
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Fiyat')
    
    # Zaman damgaları
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name='Onaylanma Tarihi')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Tamamlanma Tarihi')
    
    class Meta:
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevular'
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"{self.customer} - {self.salon.name} - {self.appointment_date} {self.appointment_time}"
    
    def save(self, *args, **kwargs):
        # Bitiş saatini otomatik hesapla
        if not self.end_time and self.service:
            from datetime import datetime, timedelta
            start_time = datetime.combine(datetime.today(), self.appointment_time)
            end_time = start_time + timedelta(minutes=self.service.duration)
            self.end_time = end_time.time()
        super().save(*args, **kwargs)

class AppointmentReview(models.Model):
    """Randevu değerlendirmeleri"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='reviews')
    
    # Değerlendirme
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name='Puan')
    comment = models.TextField(blank=True, verbose_name='Yorum')
    
    # Salon yanıtı
    salon_response = models.TextField(blank=True, verbose_name='Salon Yanıtı')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Değerlendirme Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Randevu Değerlendirmesi'
        verbose_name_plural = 'Randevu Değerlendirmeleri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer} - {self.salon.name} - {self.rating}/5"
