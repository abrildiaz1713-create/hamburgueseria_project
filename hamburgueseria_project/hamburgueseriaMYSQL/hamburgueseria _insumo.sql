use hamburgueseria;

create table insumo (
    insumo_id int auto_increment,
    nombre_insumo varchar(100) not null,
    stock_actual int not null default 0,
    unidad_medida varchar(20) not null, -- Ej: kg, unidades, litros
    primary key (insumo_id)
);