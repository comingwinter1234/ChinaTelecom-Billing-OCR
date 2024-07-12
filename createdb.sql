drop database if exists ChinaTelecom;

create database if not exists ChinaTelecom CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

use ChinaTelecom;

create table dept
(
	dept_id char(60) not null,
    dept_name char(60) not null,
    primary key(dept_id)
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;

create table class
(
	class_id char(60) not null,
    dept_id char(60) not null,
    class_name char(60) not null,
    primary key(class_id),
    foreign key(dept_id) references dept(dept_id) on update cascade on delete cascade
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;

create table worker
(
	worker_id char(60) not null,
	class_id char(60) not null,
    worker_name char(60) not null,
    role enum('normal', 'group', 'super') not null,
    pwd char(120) not null,
    primary key(worker_id),
    foreign key(class_id) references class(class_id) on update cascade on delete cascade
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;

create table service
(
	service_id char(60) not null,
--     dept_id char(60) not null,
	service_name char(60) not null,
--     service_standard char(60) not null, 
    primary key(service_id)
--     foreign key(dept_id) references dept(dept_id) on update cascade on delete cascade
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;

create table service_record
(
	service_record_id int8 not null,
	service_id char(60) not null,
--     service_name char(60) not null,
    service_time datetime,
--     dept_id char(60) not null,
    buyer_company char(60),
    seller_company char(60),
    worker_id char(60) not null,
    cost float4 not null,
    primary key(service_record_id),
    foreign key(service_id) references service(service_id) on update restrict on delete restrict,    
--     foreign key(dept_id) references dept(dept_id) on update restrict on delete restrict,
    foreign key(worker_id) references worker(worker_id) on update restrict on delete restrict
) CHARACTER SET utf8 COLLATE utf8_unicode_ci;

INSERT INTO dept (dept_id, dept_name) VALUES ('D001', 'AI与大数据部门');
INSERT INTO dept (dept_id, dept_name) VALUES ('D002', '后勤部');


INSERT INTO class (class_id, dept_id, class_name) VALUES ('C001', 'D001', '应用室');
INSERT INTO class (class_id, dept_id, class_name) VALUES ('C002', 'D001', '开发部');
INSERT INTO class (class_id, dept_id, class_name) VALUES ('C003', 'D002', '食堂');


INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W001', 'C001', '张洁铭', 'group', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W002', 'C001', '付致宁', 'super', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W003', 'C001', '黄奕', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W004', 'C001', '赵红燕', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W005', 'C001', '唐文琪', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W006', 'C001', '陈峙良', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W007', 'C001', '朱瀛', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W008', 'C002', '吴怡晨', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W009', 'C002', '丁浩', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W010', 'C002', '曹青宇', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W011', 'C003', '蔡奇', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W012', 'C003', '刘絮', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W013', 'C003', '蒋春平', 'normal', '12345');
INSERT INTO worker (worker_id, class_id, worker_name, role, pwd) VALUES ('W014', 'C003', '周晓君', 'normal', '12345');


INSERT INTO service (service_id, service_name) VALUES ('S001', '餐饮');
INSERT INTO service (service_id, service_name) VALUES ('S002', '非餐饮');

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (1, 'S001',  '2024-07-01 10:00:00', 'ChinaTelcom', 'FoodCorp', 'W001', 100.0);

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (2, 'S001' , '2024-07-02 11:00:00', 'ChinaTelcom', 'FoodCorp', 'W002', 150.0);

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (3, 'S002' , '2024-07-03 09:00:00', 'ChinaTelcom', 'TechConsult', 'W005', 500.0);

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (4, 'S001' , '2024-07-04 14:00:00', 'ChinaTelcom', 'FoodCorp', 'W003', 80.0);

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (5, 'S002' , '2024-07-05 15:00:00', 'ChinaTelcom', 'TechConsult', 'W007', 1200.0);

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (6, 'S001' , '2024-07-06 13:00:00',  'ChinaTelcom', 'FoodCorp', 'W009', 200.0);

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (7,  'S002' , '2024-07-07 16:00:00', 'ChinaTelcom', 'TechConsult', 'W011', 700.0);

INSERT INTO service_record (service_record_id, service_id, service_time,  buyer_company, seller_company, worker_id, cost) 
VALUES (8,  'S001' , '2024-07-08 12:00:00', 'ChinaTelcom', 'FoodCorp', 'W013', 250.0);

INSERT INTO service_record (service_record_id, service_id, service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (9,  'S002' , '2024-07-09 11:30:00',  'ChinaTelcom', 'TechConsult', 'W014', 600.0);

INSERT INTO service_record (service_record_id, service_id,  service_time, buyer_company, seller_company, worker_id, cost) 
VALUES (10,  'S001' , '2024-07-10 10:30:00',  'ChinaTelcom', 'FoodCorp', 'W006', 180.0);

select * from service_record;