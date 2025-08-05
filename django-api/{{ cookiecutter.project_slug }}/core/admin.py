from django.contrib import admin
from django_db_logger.models import StatusLog


admin.site.unregister(StatusLog)


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ['logger_name', 'level', 'msg', 'create_datetime']
    list_filter = ['level', 'logger_name', 'create_datetime']
    search_fields = ['msg', 'logger_name']
    readonly_fields = ['logger_name', 'level', 'msg', 'trace', 'create_datetime']
    date_hierarchy = 'create_datetime'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False