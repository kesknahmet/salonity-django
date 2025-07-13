from django.contrib import admin
from .models import Salon, SalonEmployee, SalonWorkingHours

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ['name', 'salon_type', 'city', 'district', 'rating', 'is_active', 'is_verified']
    list_filter = ['salon_type', 'city', 'is_active', 'is_verified', 'created_at']
    search_fields = ['name', 'address', 'phone', 'email']
    readonly_fields = ['rating', 'total_reviews', 'created_at', 'updated_at']
    list_editable = ['is_active', 'is_verified']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('owner', 'name', 'salon_type', 'description')
        }),
        ('İletişim Bilgileri', {
            'fields': ('address', 'city', 'district', 'phone', 'email', 'website')
        }),
        ('Çalışma Saatleri', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Değerlendirmeler', {
            'fields': ('rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Durum', {
            'fields': ('is_active', 'is_verified')
        }),
        ('Görseller', {
            'fields': ('logo', 'cover_image'),
            'classes': ('collapse',)
        }),
        ('Sosyal Medya', {
            'fields': ('instagram', 'facebook'),
            'classes': ('collapse',)
        }),
        ('Zaman Damgaları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SalonEmployee)
class SalonEmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'salon', 'position', 'is_active']
    list_filter = ['salon', 'position', 'is_active']
    search_fields = ['name', 'salon__name']
    list_editable = ['is_active']

@admin.register(SalonWorkingHours)
class SalonWorkingHoursAdmin(admin.ModelAdmin):
    list_display = ['salon', 'day_of_week', 'opening_time', 'closing_time', 'is_closed']
    list_filter = ['salon', 'day_of_week', 'is_closed']
    search_fields = ['salon__name']
