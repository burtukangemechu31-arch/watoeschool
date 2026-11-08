# inventory/admin.py
from django import forms
from django.contrib import admin
from .models import AssetCategory, SchoolAsset

class SchoolAssetAdminForm(forms.ModelForm):
    class Meta:
        model = SchoolAsset
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter asset name (e.g., Dell OptiPlex 780, Student Desk)'}),
            'serial_number': forms.TextInput(attrs={'placeholder': 'Enter unique serial number or barcode'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., IT Lab 1, Physics Laboratory, Finance Office'}),
            'purchase_cost': forms.NumberInput(attrs={'placeholder': '0.00'}),
        }

@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(SchoolAsset)
class SchoolAssetAdmin(admin.ModelAdmin):
    form = SchoolAssetAdminForm
    list_display = ('name', 'category', 'location', 'condition', 'serial_number', 'is_active')
    list_filter = ('condition', 'category', 'location', 'is_active')
    search_fields = ('name', 'serial_number', 'location')