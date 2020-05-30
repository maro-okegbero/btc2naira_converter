from django import forms


class Amount(forms.Form):
    btc_amount = forms.FloatField(required=True,  widget=forms.TextInput(attrs={'id': 'amount'}))

