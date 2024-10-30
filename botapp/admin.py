from django.contrib import admin
from .models import BotUser, BotAdmin, Position, UserRequest


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'username', 'full_name', 'language_code', 'is_active', 'created_at', 'updated_at')
    search_fields = ('id', 'user_id', 'username', 'full_name')
    list_filter = ('language_code', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')



class BotAdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_superadmin', 'created_at', 'updated_at')
    search_fields = ('id', 'user__full_name', 'user__username')
    list_filter = ('is_superadmin', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('id', 'name', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')



class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone_number', 'birth_year', 'position', 'region', 'nationality', 'education', 'marriage', 'first_answer', 'salary', 'second_answer', 'convince', 'driver_license', 'has_car', 'english_level', 'russian_level', 'other_language', 'created_at', 'updated_at')
    search_fields = ('id', 'user__full_name', 'full_name', 'phone_number', 'birth_year', 'position', 'nationality', 'education', 'region')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(BotUser, BotUserAdmin)
admin.site.register(BotAdmin, BotAdminAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(UserRequest, UserRequestAdmin)
