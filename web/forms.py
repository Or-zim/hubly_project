from django import forms
from businesses.models import Business

class BusinessCreationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'description']

        widgets ={
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название вашего бизнеса'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Краткое описание вашего бизнеса'})
        }
        
        labels = {
            'name': 'Название бизнеса',
            'description': 'Описание',
        }