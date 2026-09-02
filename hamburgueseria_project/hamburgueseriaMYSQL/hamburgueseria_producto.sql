use hamburgueseria;

create table producto(
producto_id int auto_increment,
nombre_producto varchar(100) default null,
precio_producto decimal(10,2) default null,
primary key(producto_id)
);