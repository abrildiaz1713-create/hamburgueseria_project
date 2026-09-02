from django import forms
from .models import Producto, Insumo

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'precio_producto']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Hamburguesa Doble'}),
            'precio_producto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 5500.00'}),
        }

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'cantidad', 'precio_unitario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Pan de Hamburguesa'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 50'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 1500.00'}),
        }