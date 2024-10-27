from django import forms

class TradeForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Quantity',
        'min': '1'
    }))
    
    TRADE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    action = forms.ChoiceField(label="Action", choices=TRADE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control btn btn-primary dropdown-toggle',
    }))