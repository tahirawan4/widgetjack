from django.contrib import admin

from .models import BackgroundImages, Widget, User, UsersWidgets


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_staff')
    ordering = ('-id',)


class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'is_featured')
    ordering = ('-id',)


class BackgroundAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    ordering = ('-id',)


class UsersWidgetsAdmin(admin.ModelAdmin):
    list_display = ('user', 'widget', 'click_count')
    ordering = ('-id',)


admin.site.register(User, UserAdmin)
admin.site.register(Widget, WidgetAdmin)
admin.site.register(BackgroundImages, BackgroundAdmin)
admin.site.register(UsersWidgets, UsersWidgetsAdmin)
