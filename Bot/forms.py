from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(label='Your input', max_length=100)
