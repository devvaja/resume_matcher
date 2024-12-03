from django import forms

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label="Upload Resume",
        required=True,
        widget=forms.FileInput(attrs={'accept': '.pdf'}),
    )
