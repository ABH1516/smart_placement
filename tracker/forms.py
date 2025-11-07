from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['company_name', 'job_title', 'application_date', 'status', 'notes']

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Company Name',
                'required': True
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Job Title',
                'required': True
            }),
            'application_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional notes...',
                'rows': 3
            }),
        }


# tracker/forms.py (append)
from .models import DSAProblem

class DSAProblemForm(forms.ModelForm):
    class Meta:
        model = DSAProblem
        fields = ['title', 'topic', 'status', 'date_solved']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Problem title (e.g. Two Sum - LeetCode)'}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'date_solved': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

from django import forms
from .models import AptitudeQuestion

class AptitudeQuestionForm(forms.ModelForm):
    class Meta:
        model = AptitudeQuestion
        fields = ['title', 'topic', 'status', 'solution']


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(label="Upload your Resume (PDF or DOCX)")
