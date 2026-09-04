from datetime import date, datetime

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import Insumo, Producto, ProductoInsumo


# ============================================================
# INSUMOS
# ============================================================

def listar_insumos(request):
    insumos = Insumo.objects.filter(
        estado__in=['disponible', 'por vencer']
    )

    return render(
        request,
        'gestion/listar_insumos.html',
        {
            'insumos': insumos,
            'titulo': 'Gestiï¿½n de Insumos Activos',
            'es_inactivo': False,
        }
    )


def listar_insumos_inactivos(request):
    insumos = Insumo.objects.filter(
        estado='agotado'
    )

    return render(
        request,
        'gestion/listar_insumos.html',
        {
            'insumos': insumos,
            'titulo': 'Insumos Desactivados / Agotados',
            'es_inactivo': True,
        }
    )


def crear_insumo(request):

    if request.method == 'POST':

        nombre = request.POST.get(
            'nombre_insumo',
            ''
        ).strip()

        try:
            stock_act = float(
                request.POST.get('stock_actual') or 0
            )

            stock_min = float(
                request.POST.get('stock_minimo') or 0
            )

            costo = float(
                request.POST.get('costo_unitario') or 0
            )

        except ValueError:

            messages.error(
                request,
                'Los valores numï¿½ricos ingresados no son vï¿½lidos.'
            )

            return render(
                request,
                'gestion/crear_insumo.html'
            )

        fecha_venc_str = request.POST.get(
            'fecha_vencimiento'
        )

        estado_insumo = request.POST.get(
            'estado',
            'disponible'
        )

        unidad = request.POST.get(
            'unidad_medida',
            'Unidades'
        )

        if stock_act < 0 or stock_min < 0 or costo < 0:

            messages.error(
                request,
                'Los valores de stock y costo unitario no pueden ser negativos.'
            )

            return render(
                request,
                'gestion/crear_insumo.html'
            )

        fecha_venc = None

        if fecha_venc_str:

            try:
                fecha_venc = datetime.strptime(
                    fecha_venc_str,
                    '%Y-%m-%d'
                ).date()

            except ValueError:

                messages.error(
                    request,
                    'La fecha de vencimiento no es vï¿½lida.'
                )

                return render(
                    request,
                    'gestion/crear_insumo.html'
                )

            hoy = date.today()

            if fecha_venc.year < hoy.year:

                messages.error(
                    request,
                    f'La fecha de vencimiento no puede ser de un aï¿½o anterior al actual ({hoy.year}).'
                )

                return render(
                    request,
                    'gestion/crear_insumo.html'
                )

            if fecha_venc.year > hoy.year + 100:

                messages.error(
                    request,
                    'La fecha de vencimiento supera el lï¿½mite de 100 aï¿½os.'
                )

                return render(
                    request,
                    'gestion/crear_insumo.html'
                )

        insumo_existente = Insumo.objects.filter(
            nombre_insumo__iexact=nombre
        ).first()

        if insumo_existente:

            insumo_existente.stock_actual += stock_act
            insumo_existente.stock_minimo = stock_min
            insumo_existente.costo_unitario = costo

            if fecha_venc:
                insumo_existente.fecha_vencimiento = fecha_venc

            insumo_existente.estado = estado_insumo
            insumo_existente.unidad_medida = unidad

            insumo_existente.save()

            messages.info(
                request,
                f"El insumo '{nombre}' ya existï¿½a. "
                'Se actualizï¿½ su informaciï¿½n y se sumï¿½ el stock.'
            )

        else:

            Insumo.objects.create(
                nombre_insumo=nombre,
                stock_actual=stock_act,
                stock_minimo=stock_min,
                costo_unitario=costo,
                fecha_vencimiento=fecha_venc,
                estado=estado_insumo,
                unidad_medida=unidad
            )

            messages.success(
                request,
                f"Insumo '{nombre}' registrado con ï¿½xito."
            )

        return redirect('listar_insumos')

    return render(
        request,
        'gestion/crear_insumo.html'
    )


def detalle_insumo(request, id):

    insumo = get_object_or_404(
        Insumo,
        insumo_id=id
    )

    return render(
        request,
        'gestion/detalle_insumo.html',
        {
            'insumo': insumo
        }
    )


def editar_insumo(request, id):

    insumo = get_object_or_404(
        Insumo,
        insumo_id=id
    )

    if request.method == 'POST':

        try:
            stock_act = float(
                request.POST.get('stock_actual') or 0
            )

            stock_min = float(
                request.POST.get('stock_minimo') or 0
            )

            costo = float(
                request.POST.get('costo_unitario') or 0
            )

        except ValueError:

            messages.error(
                request,
                'Los valores numï¿½ricos ingresados no son vï¿½lidos.'
            )

            return render(
                request,
                'gestion/editar_insumo.html',
                {
                    'insumo': insumo
                }
            )

        if stock_act < 0 or stock_min < 0 or costo < 0:

            messages.error(
                request,
                'Los valores de stock y costo no pueden ser negativos.'
            )

            return render(
                request,
                'gestion/editar_insumo.html',
                {
                    'insumo': insumo
                }
            )

        fecha_venc_str = request.POST.get(
            'fecha_vencimiento'
        )

        fecha_venc = None

        if fecha_venc_str:

            try:
                fecha_venc = datetime.strptime(
                    fecha_venc_str,
                    '%Y-%m-%d'
                ).date()

            except ValueError:

                messages.error(
                    request,
                    'La fecha de vencimiento no es vï¿½lida.'
                )

                return render(
                    request,
                    'gestion/editar_insumo.html',
                    {
                        'insumo': insumo
                    }
                )

            hoy = date.today()

            if (
                fecha_venc.year < hoy.year
                or fecha_venc.year > hoy.year + 100
            ):

                messages.error(
                    request,
                    'La fecha de vencimiento ingresada no es vï¿½lida o realista.'
                )

                return render(
                    request,
                    'gestion/editar_insumo.html',
                    {
                        'insumo': insumo
                    }
                )

        insumo.nombre_insumo = request.POST.get(
            'nombre_insumo',
            ''
        ).strip()

        insumo.stock_actual = stock_act
        insumo.stock_minimo = stock_min
        insumo.costo_unitario = costo
        insumo.fecha_vencimiento = fecha_venc

        insumo.estado = request.POST.get(
            'estado'
        )

        insumo.unidad_medida = request.POST.get(
            'unidad_medida'
        )

        insumo.save()

        messages.success(
            request,
            f"Insumo '{insumo.nombre_insumo}' actualizado correctamente."
        )

        return redirect('listar_insumos')

    return render(
        request,
        'gestion/editar_insumo.html',
        {
            'insumo': insumo
        }
    )


def desactivar_insumo(request, id):

    insumo = get_object_or_404(
        Insumo,
        insumo_id=id
    )

    insumo.estado = 'agotado'
    insumo.save()

    return redirect('listar_insumos')


def activar_insumo(request, id):

    insumo = get_object_or_404(
        Insumo,
        insumo_id=id
    )

    insumo.estado = 'disponible'
    insumo.save()

    return redirect('listar_insumos_inactivos')


# ============================================================
# PRODUCTOS
# ============================================================

def listar_productos(request):

    productos = Producto.objects.all().order_by(
        'nombre_producto'
    )

    return render(
        request,
        'gestion/listar_productos.html',
        {
            'productos': productos,
            'titulo': 'Gestiï¿½n de Productos',
        }
    )


def crear_producto(request):

    if request.method == 'POST':

        form = ProductoForm(request.POST)

        if form.is_valid():

            producto = form.save()

            messages.success(
                request,
                f"Producto '{producto.nombre_producto}' creado correctamente."
            )

            return redirect('listar_productos')

    else:

        form = ProductoForm()

    return render(
        request,
        'gestion/crear_producto.html',
        {
            'form': form,
            'titulo': 'Crear Producto',
        }
    )


def gestionar_ingredientes(request, producto_id):

    producto = get_object_or_404(
        Producto,
        producto_id=producto_id
    )

    ingredientes = ProductoInsumo.objects.filter(
        producto=producto
    ).select_related(
        'insumo'
    )

    insumos = Insumo.objects.filter(
        estado__in=['disponible', 'por vencer']
    ).order_by(
        'nombre_insumo'
    )

    if request.method == 'POST':

        insumo_id = request.POST.get(
            'insumo_id'
        )

        cantidad = request.POST.get(
            'cantidad'
        )

        if not insumo_id or not cantidad:

            messages.error(
                request,
                'Debe seleccionar un insumo e indicar una cantidad.'
            )

            return redirect(
                'gestionar_ingredientes',
                producto_id=producto.producto_id
            )

        try:
            cantidad = float(cantidad)

        except ValueError:

            messages.error(
                request,
                'La cantidad ingresada no es vï¿½lida.'
            )

            return redirect(
                'gestionar_ingredientes',
                producto_id=producto.producto_id
            )

        if cantidad <= 0:

            messages.error(
                request,
                'La cantidad debe ser mayor que cero.'
            )

            return redirect(
                'gestionar_ingredientes',
                producto_id=producto.producto_id
            )

        insumo = get_object_or_404(
            Insumo,
            insumo_id=insumo_id
        )

        ingrediente_existente = ProductoInsumo.objects.filter(
            producto=producto,
            insumo=insumo
        ).first()

        if ingrediente_existente:

            ingrediente_existente.cantidad = cantidad
            ingrediente_existente.save()

            messages.info(
                request,
                f"Se actualizï¿½ la cantidad de '{insumo.nombre_insumo}'."
            )

        else:

            ProductoInsumo.objects.create(
                producto=producto,
                insumo=insumo,
                cantidad=cantidad
            )

            messages.success(
                request,
                f"'{insumo.nombre_insumo}' agregado como ingrediente."
            )

        return redirect(
            'gestionar_ingredientes',
            producto_id=producto.producto_id
        )

    return render(
        request,
        'gestion/gestionar_ingredientes.html',
        {
            'producto': producto,
            'ingredientes': ingredientes,
            'insumos': insumos,
        }
    )
