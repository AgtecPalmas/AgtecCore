from core.models import Audit
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .models import Audit

class AuditAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'num_revision',
        'data_type',
        'tipo_revision',
        'ip',
        'created',
        'user_display',
        'deleted',
    )
    list_filter = (
        'data_type',
        'tipo_revision',
        'deleted',
        ('created', admin.DateFieldListFilter),
    )
    search_fields = ('ip', 'tipo_revision', 'user_change__username')
    readonly_fields = (
        'num_revision',
        'data_type',
        'tipo_revision',
        'fields_change',
        'previous_data_change',
        'current_data',
        'created',
        'user_change',
        'user_permissions_change',
        'user_groups_change',
        'ip',
        'deleted',
    )
    ordering = ('-created',)

    def user_display(self, obj):
        user = obj.user_change
        if user and isinstance(user, dict):
            return user.get('username') or user.get('email') or str(user)
        return str(user)
    user_display.short_description = _('Usuário')

    def has_add_permission(self, request):
        return False  # Auditoria só deve ser gerada pelo sistema

    def has_delete_permission(self, request, obj=None):
        return False  # Não permitir exclusão de registros de auditoria

    def has_change_permission(self, request, obj=None):
        return False  # Auditoria não deve ser editável

    def get_queryset(self, request):
        # Pode ser customizado para omitir deletados, se desejar
        return super().get_queryset(request)

admin.site.register(Audit)