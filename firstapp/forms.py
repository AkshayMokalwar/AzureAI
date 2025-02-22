# chatbot/forms.py
from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(label='Your Message', max_length=1000, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Enter your message",
        'aria-label': "Your message",
        'aria-describedby': "button-addon2"
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_input_group(self):
        """Renders the form field within an input group."""
        return f"""
        <div class="input-group mb-3">
            {self['message']}
            <button class="btn btn-outline-warning" type="button" id="button-addon2">Send</button>
        </div>
        """