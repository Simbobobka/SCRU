from django import forms

class SearchForm(forms.Form):
    
    CHOICES_site = [
        ("prom","prom"),
        ("allo",'allo'),
        ('olx','olx'),
    ]   
    
    site = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES_site, 
    )

    product = forms.CharField(
        required=True,      
        widget=forms.TextInput(),        
        )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'placeholder': 'Enter product name', 'class': 'input'})
        self.fields['site'].widget.attrs.update({'class':"checkbox", 'aria-hidden':'true'})