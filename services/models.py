from django.db import models
from salons.models import Salon, SalonEmployee
import uuid

class ServiceCategory(models.Model):
    """Hizmet kategorileri"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Kategori Adı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    icon = models.CharField(max_length=50, blank=True, verbose_name='İkon (FontAwesome)')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Hizmet Kategorisi'
        verbose_name_plural = 'Hizmet Kategorileri'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Service(models.Model):
    """Salon hizmetleri"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200, verbose_name='Hizmet Adı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Fiyat')
    duration = models.IntegerField(verbose_name='Süre (Dakika)')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    image = models.ImageField(upload_to='service_images/', blank=True, verbose_name='Hizmet Görseli')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Hizmet'
        verbose_name_plural = 'Hizmetler'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.salon.name} - {self.name}"

class ServiceEmployee(models.Model):
    """Hizmet-çalışan ilişkisi"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='employees')
    employee = models.ForeignKey(SalonEmployee, on_delete=models.CASCADE, related_name='services')
    is_available = models.BooleanField(default=True, verbose_name='Müsait')
    
    class Meta:
        verbose_name = 'Hizmet Çalışanı'
        verbose_name_plural = 'Hizmet Çalışanları'
        unique_together = ['service', 'employee']
    
    def __str__(self):
        return f"{self.service.name} - {self.employee.name}"
