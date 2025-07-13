from django.db import models
from django.contrib.auth.models import User
import uuid

class Customer(models.Model):
    LOYALTY_LEVELS = [
        ('bronze', 'Bronz'),
        ('silver', 'Gümüş'),
        ('gold', 'Altın'),
        ('platinum', 'Platin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Doğum Tarihi')
    gender = models.CharField(max_length=10, choices=[('male', 'Erkek'), ('female', 'Kadın'), ('other', 'Diğer')], blank=True, verbose_name='Cinsiyet')
    address = models.TextField(blank=True, verbose_name='Adres')
    city = models.CharField(max_length=100, blank=True, verbose_name='Şehir')
    district = models.CharField(max_length=100, blank=True, verbose_name='İlçe')
    profile_image = models.ImageField(upload_to='customer_profiles/', blank=True, verbose_name='Profil Fotoğrafı')
    
    # Sadakat sistemi
    loyalty_level = models.CharField(max_length=20, choices=LOYALTY_LEVELS, default='bronze', verbose_name='Sadakat Seviyesi')
    total_points = models.IntegerField(default=0, verbose_name='Toplam Puan')
    current_points = models.IntegerField(default=0, verbose_name='Mevcut Puan')
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Toplam Harcama')
    total_visits = models.IntegerField(default=0, verbose_name='Toplam Ziyaret')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Müşteri'
        verbose_name_plural = 'Müşteriler'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.user)
    
    def add_points(self, points, reason=""):
        """Müşteriye puan ekle"""
        self.current_points += points
        self.total_points += points
        self.save()
        
        # Puan geçmişi kaydet
        PointHistory.objects.create(
            customer=self,
            points=points,
            reason=reason
        )
        
        # Sadakat seviyesini güncelle
        self.update_loyalty_level()
    
    def use_points(self, points, reason=""):
        """Müşteri puanlarını kullan"""
        if self.current_points >= points:
            self.current_points -= points
            self.save()
            
            PointHistory.objects.create(
                customer=self,
                points=-points,
                reason=reason
            )
            return True
        return False
    
    def update_loyalty_level(self):
        """Sadakat seviyesini güncelle"""
        if self.total_spent >= 1000:
            self.loyalty_level = 'platinum'
        elif self.total_spent >= 500:
            self.loyalty_level = 'gold'
        elif self.total_spent >= 200:
            self.loyalty_level = 'silver'
        else:
            self.loyalty_level = 'bronze'
        self.save()

class PointHistory(models.Model):
    """Puan geçmişi"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='point_history')
    points = models.IntegerField(verbose_name='Puan')
    reason = models.CharField(max_length=200, verbose_name='Sebep')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Puan Geçmişi'
        verbose_name_plural = 'Puan Geçmişleri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer} - {self.points} puan - {self.reason}"
