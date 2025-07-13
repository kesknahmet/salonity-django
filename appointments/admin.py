from django.contrib import admin
from .models import Appointment, AppointmentReview

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'salon', 'service', 'appointment_date', 'appointment_time', 'status', 'price']
    list_filter = ['salon', 'status', 'appointment_date', 'created_at']
    search_fields = ['customer__user__username', 'salon__name', 'service__name']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'completed_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Randevu Bilgileri', {
            'fields': ('customer', 'salon', 'service', 'employee')
        }),
        ('Zaman Bilgileri', {
            'fields': ('appointment_date', 'appointment_time', 'end_time')
        }),
        ('Durum ve Fiyat', {
            'fields': ('status', 'price')
        }),
        ('Notlar', {
            'fields': ('notes', 'customer_notes'),
            'classes': ('collapse',)
        }),
        ('Zaman Damgaları', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AppointmentReview)
class AppointmentReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'salon', 'rating', 'created_at']
    list_filter = ['salon', 'rating', 'created_at']
    search_fields = ['customer__user__username', 'salon__name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Değerlendirme Bilgileri', {
            'fields': ('appointment', 'customer', 'salon')
        }),
        ('Değerlendirme', {
            'fields': ('rating', 'comment')
        }),
        ('Salon Yanıtı', {
            'fields': ('salon_response',),
            'classes': ('collapse',)
        }),
        ('Zaman Damgaları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
