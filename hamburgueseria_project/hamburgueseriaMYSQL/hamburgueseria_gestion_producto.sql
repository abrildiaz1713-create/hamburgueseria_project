use hamburgueseria;

CREATE TABLE `gestion_producto` (
  `gestion_id` int NOT NULL AUTO_INCREMENT,
  `accion` varchar(50) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `empleado_id` int DEFAULT NULL,
  `pedido_id` int DEFAULT NULL,
  PRIMARY KEY (`gestion_id`),
  foreign key(empleado_id) references empleado(empleado_id),
  foreign key (pedido_id) references pedidos (pedido_id)
  
  
  );