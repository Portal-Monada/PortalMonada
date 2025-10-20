from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'menu_type',
        'order',
        'parent_menu',
        'is_active',
        'is_featured',
        'created_at'
    ]

    list_filter = [
        'menu_type',
        'is_active',
        'is_featured',
        'parent_menu',
        'created_at'
    ]

    search_fields = ['title', 'url', 'icon']

    list_editable = ['order', 'is_active', 'is_featured']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'url', 'icon', 'order', 'parent_menu')
        }),
        ('Behavior', {
            'fields': ('menu_type', 'target', 'is_active', 'is_featured')
        }),
        ('Access Control', {
            'fields': ('allowed_roles', 'required_permissions'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent_menu')
