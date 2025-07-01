from django import forms
import re

class EntryForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter page title'
        })
    )
    content = forms.CharField(
        label="Content (Markdown)",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 15,
            'placeholder': 'Enter page content using Markdown syntax'
        })
    )

    def clean_title(self):
        title = self.cleaned_data['title']
        # Ensure title contains only letters, numbers, spaces, and underscores
        if not re.match(r'^[\w\s-]*$', title):
            raise forms.ValidationError(
                "Title can only contain letters, numbers, spaces, and underscores"
            )
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        # Ensure content is not too short
        if len(content.strip()) < 10:
            raise forms.ValidationError(
                "Content must be at least 10 characters long"
            )
        return content

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search Encyclopedia',
            'autocomplete': 'off'
        })
    )