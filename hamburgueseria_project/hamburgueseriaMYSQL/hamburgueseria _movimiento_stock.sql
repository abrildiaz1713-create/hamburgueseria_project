use hamburgueseria;

CREATE TABLE movimiento_stock (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_insumo INT NOT NULL,
    id_empleado INT NOT NULL,
    tipo_movimiento VARCHAR(20) NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(255),
    stock_anterior DECIMAL(10,2) NOT NULL,
    stock_posterior DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_movimiento_stock_insumo
        FOREIGN KEY (id_insumo)
        REFERENCES INSUMO(id_insumo),

    CONSTRAINT fk_movimiento_stock_empleado
        FOREIGN KEY (id_empleado)
        REFERENCES EMPLEADO(id_empleado)
);