from django.db import models

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True, db_column='producto_id')
    nombre_producto = models.CharField(max_length=100, db_column='nombre_producto')
    precio = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio')
    descripcion = models.TextField(blank=True, null=True, db_column='descripcion')

    class Meta:
        db_table = 'producto'

    def __str__(self):
        return self.nombre_producto


class Insumo(models.Model):
    insumo_id = models.AutoField(primary_key=True, db_column='insumo_id')
    nombre_insumo = models.CharField(max_length=100, db_column='nombre_insumo')
    stock_actual = models.IntegerField(default=0, db_column='stock_actual')
    stock_minimo = models.IntegerField(default=0, db_column='stock_minimo')
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, db_column='costo_unitario')
    fecha_vencimiento = models.DateField(blank=True, null=True, db_column='fecha_vencimiento')
    estado = models.CharField(max_length=50, default='disponible', db_column='estado')
    unidad_medida = models.CharField(max_length=50, default='Unidades', db_column='unidad_medida')

    class Meta:
        db_table = 'insumo'

    def __str__(self):
        return self.nombre_insumo


class ProductoInsumo(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='producto_id')
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, db_column='insumo_id')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, db_column='cantidad')

    class Meta:
        db_table = 'producto_insumo'

    def __str__(self):
        return f"{self.producto.nombre_producto} - {self.insumo.nombre_insumo} ({self.cantidad})"