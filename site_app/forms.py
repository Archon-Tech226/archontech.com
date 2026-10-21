from django import forms
from .models import Lead


class ContactForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ("Web Development", "Web Development"),
        ("Social Media Marketing", "Social Media Marketing (SMM)"),
        ("Web Application", "Web Application"),
        ("SaaS Product", "SaaS Product"),
        ("Not sure yet", "Not sure yet"),
    ]

    service = forms.ChoiceField(choices=SERVICE_CHOICES, label="What do you need?")
    # Honeypot: real visitors never fill this in; bots usually do.
    company_website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "service", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "type": "tel", "inputmode": "tel"}),
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_company_website(self):
        value = self.cleaned_data.get("company_website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value
