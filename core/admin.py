from django.contrib import admin
from .models import SiteSettings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import HomeGallery
from .models import (
    User,
    ClientProfile,
    AdvocateProfile,
    ServiceCategory,
    Service,
    Booking,
    ContactFormSubmission,
    FAQ,
    Blog,
    LegalQuery,
)


class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'user_type',
        'first_name',
        'mobile_number',
        'state',
        'city',
        'enrollment_number',
        'experience',
        'is_staff',
        'is_active'
    )
    list_filter = ('user_type', 'is_staff', 'is_active', 'state', 'city')
    search_fields = ('username', 'email', 'mobile_number', 'first_name', 'enrollment_number')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),

        ('Personal info', {
            'fields': (
                'first_name',
                'last_name',
                'mobile_number',
                'address',
                'state',
                'city',
                'profile_pic'
            )
        }),

        ('Advocate Info', {
            'fields': (
                'enrollment_number',
                'bar_council_id',
                'experience',
                'expertise',
                'document'
            )
        }),

        ('Permissions', {
            'fields': (
                'is_staff',
                'is_active',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),

        ('Important dates', {'fields': ('last_login', 'date_joined')}),

        ('User Type', {'fields': ('user_type',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'user_type',
                'mobile_number',
                'first_name',
                'state',
                'city',
                'is_staff',
                'is_active'
            )
        }),
    )

admin.site.register(User, UserAdmin)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email', 'user__mobile_number')


@admin.register(AdvocateProfile)
class AdvocateProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email', 'user__mobile_number')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'featured')
    list_filter = ('featured', 'category')
    search_fields = ('title', 'description')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'assigned_advocate', 'status', 'booking_time')
    list_filter = ('status',)
    search_fields = ('client__username', 'service__title', 'assigned_advocate__username')
    readonly_fields = ('booking_time',)


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'created_at')
    search_fields = ('name', 'email', 'mobile')
    readonly_fields = ('created_at',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question', 'answer')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content', 'meta_title', 'meta_keywords')
    readonly_fields = ('created_at',)

    fieldsets = (
        ("Blog Content", {
            "fields": ('title', 'content', 'image', 'created_at')
        }),
        ("SEO Settings", {
            "classes": ('collapse',),
            "fields": (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'canonical_url',
            )
        }),
        ("Open Graph / Social Share", {
            "classes": ('collapse',),
            "fields": (
                'og_title',
                'og_description',
                'og_image',
            )
        }),
    )



@admin.register(LegalQuery)
class LegalQueryAdmin(admin.ModelAdmin):
    list_display = ('client', 'question', 'answer', 'created_at')
    search_fields = ('client__username', 'question', 'answer')
    readonly_fields = ('created_at',)


@admin.register(HomeGallery)
class HomeGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'image')
    list_editable = ('order',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Social Media Links", {
            "fields": (
                "facebook",
                "instagram",
                "linkedin",
                "twitter",
                "youtube",
                "whatsapp",
            )
        }),
        ("Contact Information", {
            "fields": (
                "address",
                "phone",
                "email",
            )
        }),
    )

    list_display = ("id", "email", "phone")
