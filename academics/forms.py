# academics/forms.py
from django import forms
from .models import StudentProfile

class StudentRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    username = forms.CharField(max_length=150, required=True)
    
    class Meta:
        model = StudentProfile
        # Using fields matching StudentProfile model schema
        fields = [
            'student_id', 
            'program', 
            'section', 
            'parent_phone'
        ]