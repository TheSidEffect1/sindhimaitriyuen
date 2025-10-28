from django.contrib import admin
from django.utils.html import format_html
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'your_name', 'your_mob', 'city', 'state', 'gender',
        'passport_preview', 'full_preview', 'created_at'
    )

    search_fields = (
        'your_name', 'your_mob', 'father_name', 'mother_name', 'city', 'state',
    )

    readonly_fields = (
        'passport_photo_preview', 'full_photo_preview', 'created_at',
    )

    fieldsets = (
        # -------------------------
        # PAGE 1 — Basic Registration
        # -------------------------
        ('Page 1 - Personal Info', {
            'fields': (
                'your_name', 'your_mob', 'father_name', 'father_mob',
                'mother_name', 'mother_mob', 'city', 'state',
                'email', 'password', 'aadhar', 'blood_group',
                'partner_choice', 'gender',
                'passport_photo_preview', 'full_photo_preview'
            )
        }),

        # -------------------------
        # PAGE 2 — Personal Profile
        # -------------------------
        ('Page 2 - Profile Info', {
            'fields': (
                'house', 'sqft', 'floors', 'vehicles2', 'vehicles4',
                'education', 'subject', 'jobType', 'age',
                'birthDate', 'birthTime', 'birthPlace', 'skinColour',
                'height', 'weight', 'diseases', 'personalIncome',
                'jointIncome', 'company', 'position',
                'profession', 'profAddress'
            )
        }),

        # -------------------------
        # PAGE 3 — Family & Preferences
        # -------------------------
        ('Page 3 - Family & Preferences', {
            'fields': (
                'address', 'members', 'grandfather', 'grandmother',
                'father', 'mother', 'brother', 'marriedb', 'sister', 'marrieds',
                'sindh', 'nukha', 'aakay',
                'FatherBusiness', 'FatherPos','FatherBusinessAd',
                'BrotherBusiness', 'BrotherPos','BrotherBusinessAd',
                'interests', 'otherInfo',
                'widow', 'widowAccept',
                'nonVeg', 'nonVegAccept',
                'drinks', 'drinksAccept',
                'smokes', 'smokesAccept'
            )
        }),

        ('Other Info', {
            'fields': ('created_at',)
        }),
    )

    # -------------------------
    # IMAGE PREVIEWS
    # -------------------------
    def passport_preview(self, obj):
        if obj.passport_photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px;object-fit:cover;">',
                obj.passport_photo
            )
        return "—"
    passport_preview.short_description = 'Passport'

    def full_preview(self, obj):
        if obj.full_photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:6px;object-fit:cover;">',
                obj.full_photo
            )
        return "—"
    full_preview.short_description = 'Full Photo'

    def passport_photo_preview(self, obj):
        if obj.passport_photo:
            return format_html(
                '<img src="{}" width="150" style="border-radius:8px;box-shadow:0 0 5px #aaa;">',
                obj.passport_photo
            )
        return "No image uploaded."
    passport_photo_preview.short_description = "Passport Photo"

    def full_photo_preview(self, obj):
        if obj.full_photo:
            return format_html(
                '<img src="{}" width="150" style="border-radius:8px;box-shadow:0 0 5px #aaa;">',
                obj.full_photo
            )
        return "No image uploaded."
    full_photo_preview.short_description = "Full Photo"
