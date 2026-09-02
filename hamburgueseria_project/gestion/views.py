from django.shortcuts import render, redirect, get_object_or_404
from .models import Insumo

# 1. LISTAR INSUMOS ACTIVOS
def listar_insumos(request):
    insumos = Insumo.objects.filter(estado__in=['disponible', 'por vencer'])
    return render(request, 'gestion/listar_insumos.html', {
        'insumos': insumos,
        'titulo': 'Gestión de Insumos Activos',
        'es_inactivo': False
    })

# 2. LISTAR INSUMOS INACTIVOS / AGOTADOS
def listar_insumos_inactivos(request):
    insumos = Insumo.objects.filter(estado='agotado')
    return render(request, 'gestion/listar_insumos.html', {
        'insumos': insumos,
        'titulo': 'Insumos Desactivados / Agotados',
        'es_inactivo': True
    })

# 3. CREAR NUEVO INSUMO
def crear_insumo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_insumo')
        stock_act = request.POST.get('stock_actual')
        stock_min = request.POST.get('stock_minimo')
        costo = request.POST.get('costo_unitario')
        fecha_venc = request.POST.get('fecha_vencimiento') or None
        estado_insumo = request.POST.get('estado')
        unidad = request.POST.get('unidad_medida')

        Insumo.objects.create(
            nombre_insumo=nombre,
            stock_actual=stock_act,
            stock_minimo=stock_min,
            costo_unitario=costo,
            fecha_vencimiento=fecha_venc,
            estado=estado_insumo,
            unidad_medida=unidad
        )
        return redirect('listar_insumos')
    return render(request, 'gestion/crear_insumo.html')

# 4. VER DETALLE DE INSUMO (VISTA OJO)
def detalle_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)
    return render(request, 'gestion/detalle_insumo.html', {'insumo': insumo})

# 5. EDITAR INSUMO
def editar_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)
    if request.method == 'POST':
        insumo.nombre_insumo = request.POST.get('nombre_insumo')
        insumo.stock_actual = request.POST.get('stock_actual')
        insumo.stock_minimo = request.POST.get('stock_minimo')
        insumo.costo_unitario = request.POST.get('costo_unitario')
        insumo.fecha_vencimiento = request.POST.get('fecha_vencimiento') or None
        insumo.estado = request.POST.get('estado')
        insumo.unidad_medida = request.POST.get('unidad_medida')
        insumo.save()
        return redirect('listar_insumos')
    return render(request, 'gestion/editar_insumo.html', {'insumo': insumo})

# 6. DESACTIVAR INSUMO (SOFT DELETE)
def desactivar_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)
    insumo.estado = 'agotado'
    insumo.save()
    return redirect('listar_insumos')

# 7. ACTIVAR INSUMO
def activar_insumo(request, id):
    insumo = get_object_or_404(Insumo, insumo_id=id)
    insumo.estado = 'disponible'
    insumo.save()
    return redirect('listar_insumos_inactivos')