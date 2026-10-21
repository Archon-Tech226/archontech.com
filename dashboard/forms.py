from django import forms
from site_app.models import BlogPost, Testimonial, PortfolioProject, Lead


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["author_name", "title", "category", "excerpt", "body", "status"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 14}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["client_name", "company", "quote", "rating", "is_published", "is_sample"]
        widgets = {
            "quote": forms.Textarea(attrs={"rows": 4}),
            "rating": forms.Select(choices=[(i, f"{i} star{'s' if i != 1 else ''}") for i in range(1, 6)]),
        }


class PortfolioProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioProject
        fields = ["title", "description", "image", "category", "project_type", "tech_tags", "live_url", "is_published", "sort_order"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class LeadStatusForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["status", "follow_up_date", "notes"]
        widgets = {
            "follow_up_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
