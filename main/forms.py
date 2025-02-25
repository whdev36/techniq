# from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from .models import Player
from .form_attrs import field_attrs

class PlayerCreationForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically update field attributes
        for field, attr in field_attrs.items():
            if field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': attr.get('placeholder', ''),
                    'required': True,
                })
                self.fields[field].label = attr.get('label', '')
                self.fields[field].label_suffix = ' *'
                self.fields[field].help_text = attr.get('help_text', '')
                self.fields[field].error_messages = attr.get('error_messages', '')

    def as_div(self):
        '''Render the form fields as Bootstrap-styled <div> elements.'''
        return mark_safe(
            '\n'.join(
                f'<div class="form-group mb-3">'
                f'{field.label_tag()}{field}'
                f'{"".join(f"<div class=\"text-danger\">{error}</div>" for error in field.errors)}'
                f'{"".join(f"<small class=\"text-muted\">{field.help_text}</small>")}'
                f'</div>'
                if not field.is_hidden else str(field)
                for field in self
            )
        )