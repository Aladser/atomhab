from django.contrib import admin
from authen_drf.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'last_login')
    search_fields = ('first_name', 'last_name', 'email')
