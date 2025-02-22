field_attrs = {
    'first_name': {
        'placeholder': 'Ismingizni kiriting',
        'label': 'Ism',
        'help_text': 'Iltimos, ismingizni kiriting.',
        'error_messages': {
            'required': 'Ism kiritish majburiy.',
            'max_length': 'Ism 100 belgidan oshmasligi kerak.'
        }
    },
    'last_name': {
        'placeholder': 'Familiyangizni kiriting',
        'label': 'Familiya',
        'help_text': 'Iltimos, familiyangizni kiriting.',
        'error_messages': {
            'required': 'Familiya kiritish majburiy.',
            'max_length': 'Familiya 100 belgidan oshmasligi kerak.'
        }
    },
    'email': {
        'placeholder': 'Emailingizni kiriting',
        'label': 'Email manzili',
        'help_text': 'Biz hech qachon email manzilingizni boshqalar bilan ulashmaymiz.',
        'error_messages': {
            'required': 'Iltimos, email manzilingizni kiriting.',
            'invalid': 'Iltimos, to‘g‘ri email manzil kiriting.'
        }
    },
    'username': {
        'placeholder': 'Foydalanuvchi nomini kiriting',
        'label': 'Foydalanuvchi nomi',
        'help_text': 'Yangi va unik al foydalanuvchi nomini tanlang.',
        'error_messages': {
            'required': 'Foydalanuvchi nomi majburiy.',
            'max_length': 'Foydalanuvchi nomi 150 belgidan oshmasligi kerak.'
        }
    },
    'password1': {
        'placeholder': 'Parolingizni kiriting',
        'label': 'Parol',
        'help_text': 'Parolingiz kamida 8 ta belgidan iborat bo‘lishi kerak.',
        'error_messages': {
            'required': 'Parol kiritish majburiy.',
        }
    },
    'password2': {
        'placeholder': 'Parolingizni tasdiqlang',
        'label': 'Parolni tasdiqlang',
        'help_text': 'Parolingizni qayta kiriting.',
        'error_messages': {
            'required': 'Iltimos, parolingizni tasdiqlang.',
            'password_mismatch': 'Kiritilgan parollar mos kelmadi.'
        }
    }
}