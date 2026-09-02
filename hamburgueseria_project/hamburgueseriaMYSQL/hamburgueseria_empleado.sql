use hamburgueseria;

CREATE TABLE `empleado` (
  `empleado_id` int NOT NULL AUTO_INCREMENT,
  `nombre_empleado` varchar(50) DEFAULT NULL,
  `rol_empleado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`empleado_id`)
) 