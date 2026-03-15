from django import forms

class SubjectForm(forms.Form):
    subject = forms.CharField(max_length=100)