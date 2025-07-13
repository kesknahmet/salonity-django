from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Salon(models.Model):
    SALON_TYPES = [
        ('kuafor', 'Kuaför'),
        ('berber', 'Berber'),
        ('guzellik_salonu', 'Güzellik Salonu'),
        ('spa', 'Spa & Masaj'),
        ('manikur', 'Manikür & Pedikür'),
        ('diger', 'Diğer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_salons')
    name = models.CharField(max_length=200, verbose_name='Salon Adı')
    salon_type = models.CharField(max_length=20, choices=SALON_TYPES, verbose_name='Salon Türü')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    address = models.TextField(verbose_name='Adres')
    city = models.CharField(max_length=100, verbose_name='Şehir')
    district = models.CharField(max_length=100, verbose_name='İlçe')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    email = models.EmailField(blank=True, verbose_name='E-posta')
    website = models.URLField(blank=True, verbose_name='Web Sitesi')
    
    # Çalışma saatleri
    opening_time = models.TimeField(verbose_name='Açılış Saati')
    closing_time = models.TimeField(verbose_name='Kapanış Saati')
    
    # Salon özellikleri
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Ortalama Puan')
    total_reviews = models.IntegerField(default=0, verbose_name='Toplam Değerlendirme')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    is_verified = models.BooleanField(default=False, verbose_name='Doğrulanmış')
    
    # Görsel
    logo = models.ImageField(upload_to='salon_logos/', blank=True, verbose_name='Logo')
    cover_image = models.ImageField(upload_to='salon_covers/', blank=True, verbose_name='Kapak Fotoğrafı')
    
    # Sosyal medya
    instagram = models.URLField(blank=True, verbose_name='Instagram')
    facebook = models.URLField(blank=True, verbose_name='Facebook')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    
    class Meta:
        verbose_name = 'Salon'
        verbose_name_plural = 'Salonlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        """Ortalama puanı hesapla"""
        if self.total_reviews > 0:
            return self.rating
        return 0.00

class SalonEmployee(models.Model):
    """Salon çalışanları"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=100, verbose_name='Ad Soyad')
    position = models.CharField(max_length=100, verbose_name='Pozisyon')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    email = models.EmailField(blank=True, verbose_name='E-posta')
    bio = models.TextField(blank=True, verbose_name='Hakkında')
    photo = models.ImageField(upload_to='employee_photos/', blank=True, verbose_name='Fotoğraf')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Salon Çalışanı'
        verbose_name_plural = 'Salon Çalışanları'
    
    def __str__(self):
        return f"{self.name} - {self.salon.name}"

class SalonWorkingHours(models.Model):
    """Salon çalışma saatleri (günlük)"""
    DAYS_OF_WEEK = [
        (0, 'Pazartesi'),
        (1, 'Salı'),
        (2, 'Çarşamba'),
        (3, 'Perşembe'),
        (4, 'Cuma'),
        (5, 'Cumartesi'),
        (6, 'Pazar'),
    ]
    
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name='Gün')
    opening_time = models.TimeField(verbose_name='Açılış Saati')
    closing_time = models.TimeField(verbose_name='Kapanış Saati')
    is_closed = models.BooleanField(default=False, verbose_name='Kapalı')
    
    class Meta:
        verbose_name = 'Çalışma Saati'
        verbose_name_plural = 'Çalışma Saatleri'
        unique_together = ['salon', 'day_of_week']
    
    def __str__(self):
        day_name = dict(self.DAYS_OF_WEEK)[int(self.day_of_week)]
        if self.is_closed:
            return f"{self.salon.name} - {day_name} (Kapalı)"
        return f"{self.salon.name} - {day_name} ({self.opening_time}-{self.closing_time})"

class Campaign(models.Model):
    """Salon kampanyaları"""
    CAMPAIGN_TYPES = [
        ('discount', 'İndirim'),
        ('free_service', 'Ücretsiz Hizmet'),
        ('bonus_points', 'Bonus Puan'),
        ('loyalty_discount', 'Sadakat İndirimi'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='campaigns')
    name = models.CharField(max_length=200, verbose_name='Kampanya Adı')
    description = models.TextField(verbose_name='Açıklama')
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES, verbose_name='Kampanya Türü')
    
    # İndirim bilgileri
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True, verbose_name='İndirim Yüzdesi')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='İndirim Tutarı')
    bonus_points = models.IntegerField(null=True, blank=True, verbose_name='Bonus Puan')
    
    # Tarih aralığı
    start_date = models.DateField(verbose_name='Başlangıç Tarihi')
    end_date = models.DateField(verbose_name='Bitiş Tarihi')
    
    # Kullanım limitleri
    max_usage = models.IntegerField(null=True, blank=True, verbose_name='Maksimum Kullanım')
    current_usage = models.IntegerField(default=0, verbose_name='Mevcut Kullanım')
    
    # Durum
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Kampanya'
        verbose_name_plural = 'Kampanyalar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.salon.name} - {self.name}"
    
    def is_valid(self):
        """Kampanya geçerli mi kontrol et"""
        from datetime import date
        today = date.today()
        return (self.is_active and 
                self.start_date <= today <= self.end_date and
                (self.max_usage is None or self.current_usage < self.max_usage))

class Coupon(models.Model):
    """Kupon sistemi"""
    COUPON_TYPES = [
        ('percentage', 'Yüzde İndirim'),
        ('fixed', 'Sabit İndirim'),
        ('free_service', 'Ücretsiz Hizmet'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=20, unique=True, verbose_name='Kupon Kodu')
    name = models.CharField(max_length=200, verbose_name='Kupon Adı')
    description = models.TextField(verbose_name='Açıklama')
    coupon_type = models.CharField(max_length=20, choices=COUPON_TYPES, verbose_name='Kupon Türü')
    
    # İndirim bilgileri
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True, verbose_name='İndirim Yüzdesi')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='İndirim Tutarı')
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Minimum Tutar')
    
    # Tarih aralığı
    start_date = models.DateField(verbose_name='Başlangıç Tarihi')
    end_date = models.DateField(verbose_name='Bitiş Tarihi')
    
    # Kullanım limitleri
    max_usage = models.IntegerField(null=True, blank=True, verbose_name='Maksimum Kullanım')
    current_usage = models.IntegerField(default=0, verbose_name='Mevcut Kullanım')
    
    # Durum
    is_active = models.BooleanField(default=True, verbose_name='Aktif')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Kupon'
        verbose_name_plural = 'Kuponlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def is_valid(self):
        """Kupon geçerli mi kontrol et"""
        from datetime import date
        today = date.today()
        return (self.is_active and 
                self.start_date <= today <= self.end_date and
                (self.max_usage is None or self.current_usage < self.max_usage))
