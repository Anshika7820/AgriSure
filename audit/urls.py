from django.urls import path
from . import views

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/verifications/", views.admin_verifications_list, name="admin_verifications"),
    path("admin-dashboard/verifications/<int:doc_id>/action/", views.admin_verify_action, name="admin_verify_action"),
    path("admin-dashboard/users/", views.admin_users_list, name="admin_users"),
    path("admin-dashboard/users/<int:user_id>/toggle-active/", views.admin_user_toggle_active, name="admin_user_toggle_active"),
    path("admin-dashboard/audit-logs/", views.admin_audit_logs, name="admin_audit_logs"),
]
