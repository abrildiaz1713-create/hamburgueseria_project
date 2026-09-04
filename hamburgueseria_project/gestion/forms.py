from django import forms
from .models import Producto, Insumo


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            'nombre_producto',
            'precio',
            'descripcion',
        ]

        widgets = {
            'nombre_producto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Hamburguesa Doble',
                }
            ),

            'precio': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 5500.00',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripción del producto',
                    'rows': 3,
                }
            ),
        }


class InsumoForm(forms.ModelForm):

    class Meta:
        model = Insumo

        fields = [
            'nombre_insumo',
            'stock_actual',
            'stock_minimo',
            'costo_unitario',
            'fecha_vencimiento',
            'estado',
            'unidad_medida',
        ]

        widgets = {
            'nombre_insumo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Pan de Hamburguesa',
                }
            ),

            'stock_actual': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 50',
                    'min': '0',
                }
            ),

            'stock_minimo': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 10',
                    'min': '0',
                }
            ),

            'costo_unitario': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 1500.00',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'fecha_vencimiento': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                }
            ),

            'estado': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'unidad_medida': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Unidades, Kg, Gramos',
                }
            ),
        }
