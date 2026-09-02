use hamburgueseria;
create table detalle_pedido(
detalle_pedido_id int auto_increment,
producto_id int NOT NULL,
pedido_id int not null,
cantidad varchar(50) DEFAULT NULL,
precio_unitario decimal(10,2) DEFAULT NULL,
PRIMARY KEY (detalle_pedido_id),
foreign key (pedido_id) references pedidos(pedido_id),
foreign key (producto_id) references producto(producto_id));
