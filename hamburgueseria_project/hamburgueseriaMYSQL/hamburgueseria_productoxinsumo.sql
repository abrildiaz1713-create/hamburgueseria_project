use hamburgueseria;

CREATE TABLE productoxinsumo (
    id_producto_insumo INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    id_insumo INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,

    CONSTRAINT fk_producto_insumo_producto
        FOREIGN KEY (id_producto)
        REFERENCES PRODUCTO(id_producto),

    CONSTRAINT fk_producto_insumo_insumo
        FOREIGN KEY (id_insumo)
        REFERENCES INSUMO(id_insumo)
);