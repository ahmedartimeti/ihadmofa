from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role', 'department', 'section', 'job_title')
    list_filter = ('role', 'department', 'section')
    search_fields = ('full_name', 'user__username', 'department', 'section')
