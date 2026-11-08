# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.html import format_html

User = get_user_model()

class CustomAdminPasswordChangeForm(AdminPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholders to password input fields
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Enter new secure password (min. 8 characters)'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm new password'
        })

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Bind the custom form to the admin password change view
    change_password_form = CustomAdminPasswordChangeForm
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_staff', 'change_password_link')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Wato IMS Profile Info', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Wato IMS Profile Info', {'fields': ('role', 'phone', 'first_name', 'last_name', 'email')}),
    )

    def change_password_link(self, obj):
        return format_html(
            '<a class="button" href="{}" style="background:#0284c7; color:white; padding:4px 8px; border-radius:4px; text-decoration:none; font-weight:bold;">Change Password</a>',
            f'/admin/accounts/user/{obj.id}/password/'
        )
    change_password_link.short_description = "Password Action"