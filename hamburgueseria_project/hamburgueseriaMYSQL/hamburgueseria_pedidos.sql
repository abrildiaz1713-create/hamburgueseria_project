use hamburgueseria;
create table pedidos(
pedido_id int auto_increment,
fecha_pedido datetime default null,
cliente_id int default null,
primary key (pedido_id),
foreign key (cliente_id) references cliente(cliente_id)  
);

alter table pedidos add column estdo varchar(100) default 'pendiente';
alter table pedidos change column estdo estado varchar(100) default 'pemdiente'; 
alter table pedidos modify column fecha_pedido datetime default current_timestamp; 