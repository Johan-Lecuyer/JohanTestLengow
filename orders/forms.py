from django import forms


class FluxXMLForm(forms.Form):
    flux_url = forms.URLField(
        label='Flux XML URL',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'value': 'http://test.lengow.io/orders-test.xml'}),
        required=True
        )
