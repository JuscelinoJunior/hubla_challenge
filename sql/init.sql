create database if not exists hubla_sales;
use hubla_sales;

create table hubla_sales.sale_type
(
    sale_type_id int        not null
        primary key,
    description  varchar(40)       not null,
    kind         varchar(40)       not null,
    sign         varchar(1) not null
);


create table hubla_sales.sale
(
    sale_id int auto_increment
        primary key,
    type    int      not null,
    date    datetime null,
    product varchar(40)     not null,
    value   float    not null,
    seller  varchar(40)     not null,
    constraint sale_type___fk
        foreign key (type) references hubla_sales.sale_type (sale_type_id)
);

insert into sale_type VALUES (1, 'Venda produtor', 'Entrada', '+');
insert into sale_type VALUES (2, 'Venda afiliado', 'Entrada', '+');
insert into sale_type VALUES (3, 'Comissão paga', 'Saída', '-');
insert into sale_type VALUES (4, 'Comissão recebida', 'Entrada', '+');