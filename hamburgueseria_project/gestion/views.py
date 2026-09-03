from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import date, datetime
from .models import Insumo


# --- 1. LISTAR INSUMOS ACTIVOS ---
def listar_insumos(request):
    insumos = Insumo.objects.filter(estado__in=['disponible', 'por vencer'])
    return render(request, 'gestion/listar_insumos.html', {
        'insumos': insumos,
        'titulo': 'Gestión de Insumos Activos',
        'es_inactivo': False
    })


# --- 2. LISTAR INSUMOS INACTIVOS / AGOTADOS ---
def listar_insumos_inactivos(request):
    insumos = Insumo.objects.filter(estado='agotado')
    return render(request, 'gestion/listar_insumos.html', {
        'insumos': insumos,
        'titulo': 'Insumos Desactivados / Agotados',
        'es_inactivo': True
    })


# --- 3. CREAR / ACTUALIZAR INSUMO CON VALIDACIONES Y DUPLICADOS ---
def crear_insumo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_insumo', '').strip()
        stock_act = float(request.POST.get('stock_actual') or 0)
        stock_min = float(request.POST.get('stock_minimo') or 0)
        costo = float(request.POST.get('costo_unitario') or 0)
        fecha_venc_str = request.POST.get('fecha_vencimiento')
        estado_insumo = request.POST.get('estado', 'disponible')
        unidad = request.POST.get('unidad_medida', 'Unidades')

        # --- VALIDACIÓN 1: NÚMEROS NO NEGATIVOS ---
        if stock_act < 0 or stock_min < 0 or costo < 0:
            messages.error(request, "Los valores de stock y costo unitario no pueden ser negativos.")
            return render(request, 'gestion/crear_insumo.html')

        # --- VALIDACIÓN 2: FECHA DE VENCIMIENTO REALISTA ---
        fecha_venc = None
        if fecha_venc_str:
            fecha_venc = datetime.strptime(fecha_venc_str, '%Y-%m-%d').date()
            hoy = date.today()
            
            if fecha_venc.year < hoy.year:
                messages.error(request, f"La fecha de vencimiento no puede ser de un año anterior al actual ({hoy.year}).")
                return render(request, 'gestion/crear_insumo.html')
            
            if fecha_venc.year > hoy.year + 100:
                messages.error(request, "La fecha de vencimiento supera el límite de realismo (máximo 100 años).")
                return render(request, 'gestion/crear_insumo.html')

        # --- VALIDACIÓN 3: DUPLICADOS Y ACTUALIZACIÓN AUTOMÁTICA ---
        insumo_existente = Insumo.objects.filter(nombre_insumo__iexact=nombre).first()

        if insumo_existente:
            insumo_existente.stock_actual += stock_act
            insumo_existente.stock_minimo = stock_min
            insumo_existente.costo_unitario = costo
            if fecha_venc:
                insumo_existente.fecha_vencimiento = fecha_venc
            insumo_existente.estado = estado_insumo
            insumo_existente.unidad_medida = unidad
            insumo_existente.save()

            messages.info(request, f"El insumo '{nombre}' ya existía. Se actualizó su información y se sumó el stock.")
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
            messages.success(request, f"Insumo '{nombre}' registrado con éxito.")

        return redirect('listar_insumos')

    return render(request, 'gestion/crear_insumo.html')


# --- 4. DETALLE DE INSUMO (VISTA OJO) ---
def detalle_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)
    return render(request, 'gestion/detalle_insumo.html', {'insumo': insumo})


# --- 5. EDITAR INSUMO CON VALIDACIONES ---
def editar_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)

    if request.method == 'POST':
        stock_act = float(request.POST.get('stock_actual') or 0)
        stock_min = float(request.POST.get('stock_minimo') or 0)
        costo = float(request.POST.get('costo_unitario') or 0)
        fecha_venc_str = request.POST.get('fecha_vencimiento')

        if stock_act < 0 or stock_min < 0 or costo < 0:
            messages.error(request, "Los valores de stock y costo no pueden ser negativos.")
            return render(request, 'gestion/editar_insumo.html', {'insumo': insumo})

        fecha_venc = None
        if fecha_venc_str:
            fecha_venc = datetime.strptime(fecha_venc_str, '%Y-%m-%d').date()
            hoy = date.today()
            if fecha_venc.year < hoy.year or fecha_venc.year > hoy.year + 100:
                messages.error(request, "La fecha de vencimiento ingresada no es válida o realista.")
                return render(request, 'gestion/editar_insumo.html', {'insumo': insumo})

        insumo.nombre_insumo = request.POST.get('nombre_insumo', '').strip()
        insumo.stock_actual = stock_act
        insumo.stock_minimo = stock_min
        insumo.costo_unitario = costo
        insumo.fecha_vencimiento = fecha_venc
        insumo.estado = request.POST.get('estado')
        insumo.unidad_medida = request.POST.get('unidad_medida')
        insumo.save()

        messages.success(request, f"Insumo '{insumo.nombre_insumo}' actualizado correctamente.")
        return redirect('listar_insumos')

    return render(request, 'gestion/editar_insumo.html', {'insumo': insumo})


# --- 6. ACCIONES DE ACTIVACIÓN / DESACTIVACIÓN (SOFT DELETE) ---
def desactivar_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)
    insumo.estado = 'agotado'
    insumo.save()
    return redirect('listar_insumos')


def activar_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)
    insumo.estado = 'disponible'
    insumo.save()
    return redirect('listar_insumos_inactivos')