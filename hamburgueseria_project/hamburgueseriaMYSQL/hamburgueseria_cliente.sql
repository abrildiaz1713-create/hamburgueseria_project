create database hamburgueseria;
use hamburgueseria;
create table cliente(
cliente_id int auto_increment,
nombre varchar (100) default null,
apellido varchar(100) default null,
email varchar(100) default null,
direccion varchar (100) default null,
primary key(cliente_id ));