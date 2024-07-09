from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "txtUsername",
                "autocomplete": False,
                "autofocus": True,
                "required": True,
                "placeholder": "User Name",
            }
        ),
    )
    email = forms.EmailField(
        label="",
        max_length=250,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "txtEmail",
                "autocomplete": False,
                "required": True,
                "placeholder": "Email",
            }
        ),
    )
    password = forms.CharField(
        label="",
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "txtPassword",
                "autocomplete": False,
                "required": True,
                "placeholder": "Password",
            }
        ),
    )

class LoginInForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "txtUsername",
                "autocomplete": False,
                "autofocus": True,
                "required": True,
                "placeholder": "User Name",
            }
        ),
        error_messages={
            'required': 'Please enter your username.',
            'max_length': 'username cannot exceed 50 characters.',
        }
    )
    password = forms.CharField(
        label="",
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "txtPassword",
                "autocomplete": False,
                "required": True,
                "placeholder": "Password",
            }
        ),
        error_messages={
            'required': 'Please enter your username.',
            'max_length': 'username cannot exceed 50 characters.',
        }
    )


class NotesForm(forms.Form):
    title = forms.CharField(
        label="",
        max_length=250,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "txtTitle",
                "autocomplete": False,
                "required": True,
                "placeholder": "Title",
            }
        )
    )
    body = forms.CharField(
        label="",
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "txtNote",
                "autocomplete": False,
                "required": True,
                "placeholder": "Notes",
            }
        )
    )