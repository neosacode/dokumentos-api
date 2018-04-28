from django.contrib import admin
from apps.documents.models import Country, Document, Model, Type

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def log_addition(self, *args, **kwargs):
        pass

    def log_change(self, *args, **kwargs):
        pass

    def log_deletion(self, *args, **kwargs):
        pass


@admin.register(Document)
class DocumentAdmin(BaseAdmin):
    list_display = ['__str__', 'ref', 'error', 'file', 'webhook', 'request_id', 'is_ready', 'status', 'created']
    list_filter = ['status']
    search_fields = ['request_id', 'user__username', 'user__email']
    readonly_fields = ['model', 'status', 'user', 'is_ready', 'error', 'webhook', 'tries', 'contains', 'ref', 'file', 'request_id']