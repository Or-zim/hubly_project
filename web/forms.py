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

class ProductVariantForm(forms.Form):
    price = forms.DecimalField(
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        label="Цена за товар",
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg border-start-0', 
            'style': 'background: #050505;',
            'placeholder': '0.00'
        })
    )
    def __init__(self, *args, product_type_fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if product_type_fields:
            for field in product_type_fields:
                field_name = f"field_{field['name']}"
                field_type = field.get('type', 'text') 

                if field_type == 'number':
                    unit = field.get('unit', '')
                    self.fields[field_name] = forms.FloatField(
                        label=field['label'],
                        required=True,
                        min_value=0.1,
                        widget=forms.NumberInput(attrs={
                            'class': 'form-control form-control-lg',
                            'style': 'background: #050505;',
                            'placeholder': f"Введите число (напр: 250)",
                            'data-unit': unit
                        })
                    )
                else:
                    self.fields[field_name] = forms.CharField(
                        label=field['label'],
                        required=True,
                        widget=forms.TextInput(attrs={
                            'class': 'form-control form-control-lg',
                            'style': 'background: #050505;',
                            'placeholder': f"Введите {field['label'].lower()}"
                        })
                    )

    