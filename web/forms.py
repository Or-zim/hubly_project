from django import forms
from businesses.models import Business
from catalog.models import ProductVariant


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

class StockInboundForm(forms.Form):
    variant = forms.ModelChoiceField(
        queryset=ProductVariant.objects.none(), 
        label="Выберите товар",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity = forms.IntegerField(
        min_value=1, 
        label="Количество",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сколько штук приехало?'})
    )
    reason = forms.CharField(
        required=False, 
        label="Комментарий",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Напр: Поставка от Иванова'})
    )

    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business')
        super().__init__(*args, **kwargs)
        self.fields['variant'].queryset = ProductVariant.objects.filter(product__business=business)
    