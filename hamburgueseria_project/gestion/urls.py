from django.urls import path
from . import views

urlpatterns = [
    path('insumos/', views.listar_insumos, name='listar_insumos'),
    path('insumos/inactivos/', views.listar_insumos_inactivos, name='listar_insumos_inactivos'), # <-- RUTA QUE FALTABA
    path('insumos/nuevo/', views.crear_insumo, name='crear_insumo'),
    path('insumos/detalle/<int:id>/', views.detalle_insumo, name='detalle_insumo'),
    path('insumos/editar/<int:id>/', views.editar_insumo, name='editar_insumo'),
    path('insumos/desactivar/<int:id>/', views.desactivar_insumo, name='desactivar_insumo'),
    path('insumos/activar/<int:id>/', views.activar_insumo, name='activar_insumo'),
]