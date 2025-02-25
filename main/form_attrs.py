field_attrs = {
    'username': {
        'placeholder': 'Enter your username',
        'label': 'Username',
        'help_text': 'Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.',
        'error_messages': {
            'required': 'This field is required.',
            'unique': 'A user with that username already exists.',
        },
    },
    'password1': {
        'placeholder': 'Enter your password',
        'label': 'Password',
        'help_text': 'Your password must contain at least 8 characters and cannot be entirely numeric.',
        'error_messages': {
            'required': 'This field is required.',
        },
    },
    'password2': {
        'placeholder': 'Confirm your password',
        'label': 'Confirm Password',
        'help_text': 'Enter the same password as before, for verification.',
        'error_messages': {
            'required': 'This field is required.',
        },
    },
}