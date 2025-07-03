from django.contrib import admin
from .models import Photo, Profile
from django.utils.html import format_html

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'uploaded_at', 'thumbnail_preview')
    search_fields = ('title', 'description', 'user__username')
    list_filter = ('uploaded_at', 'user')

    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;" />', obj.image.url)
        return "-"
    thumbnail_preview.short_description = "Preview"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_pic_preview')
    search_fields = ('user__username', 'bio')

    def profile_pic_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="40" height="40" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "-"
    profile_pic_preview.short_description = "Profile Pic"
