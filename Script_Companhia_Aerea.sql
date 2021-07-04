DROP SCHEMA IF EXISTS COMPANHIA_AEREA;
BEGIN;
CREATE SCHEMA COMPANHIA_AEREA;
USE COMPANHIA_AEREA;

CREATE TABLE AEROPORTO(
	Codigo_aeroporto VARCHAR(5),
    Nome VARCHAR(45) NOT NULL,
    Cidade VARCHAR(45) NOT NULL,
    Estado VARCHAR(45),
	PRIMARY KEY(Codigo_aeroporto)
);

CREATE TABLE VOO(
	Numero_voo VARCHAR(6),
    Companhia_aerea VARCHAR(45) NOT NULL,
    Dias_da_semana VARCHAR(45) NOT NULL,
    PRIMARY KEY(Numero_voo)
);

CREATE TABLE TRECHO_VOO(
	Numero_voo VARCHAR(6),
    Numero_trecho INT,
    Codigo_aeroporto_partida VARCHAR(5),
    Horario_partida_previsto VARCHAR(10),
    Codigo_aeroporto_chegada VARCHAR(5),
    Horario_chegada_previsto VARCHAR(10),
	PRIMARY KEY(Numero_voo, Numero_trecho)
);

CREATE TABLE INSTANCIA_TRECHO(
	Numero_voo VARCHAR(6),
    Numero_trecho INT,
    Data_instancia_trecho DATE,
    Numero_assentos_disponiveis VARCHAR(45),
    Codigo_aeronave VARCHAR(5),
    Codigo_aeroporto_partida VARCHAR(5) NOT NULL,
    Horario_partida VARCHAR(10),
    Codigo_aeroporto_chegada VARCHAR(5) NOT NULL,
    Horario_chegada VARCHAR(10),
    PRIMARY KEY (Numero_voo, Numero_trecho, Data_instancia_trecho)
);

CREATE TABLE TARIFA(
	Numero_voo VARCHAR(6),
    Codigo_tarifa INT,
    Quantidade INT,
    Restricoes VARCHAR(50),
    PRIMARY KEY(Numero_voo, Codigo_tarifa)
);

CREATE TABLE TIPO_AERONAVE(
	Nome_tipo_aeronave VARCHAR(20),
    Qtd_max_assentos VARCHAR(10), 
    Companhia VARCHAR(45),
    PRIMARY KEY(Nome_tipo_aeronave)
);

CREATE TABLE PODE_POUSAR(
	Nome_tipo_aeronave VARCHAR(45),
    Codigo_aeroporto VARCHAR(5),
    PRIMARY KEY (Nome_tipo_aeronave, Codigo_aeroporto)
);

CREATE TABLE AERONAVE(
	Codigo_aeronave VARCHAR(5),
    Numero_total_assentos VARCHAR(10),
    Tipo_aeronave VARCHAR(20),
    PRIMARY KEY(Codigo_aeronave)
);

CREATE TABLE RESERVA_ASSENTO(
	Numero_voo VARCHAR(6),
    Numero_trecho INT,
    Data_reserva_assento DATE,
    Numero_assento VARCHAR(10),
	Nome_cliente VARCHAR(50),
    Telefone_cliente VARCHAR(10),
    PRIMARY KEY(Numero_voo, Numero_trecho, Data_reserva_assento, Numero_assento)
);

ALTER TABLE AERONAVE ADD FOREIGN KEY(Tipo_aeronave) REFERENCES TIPO_AERONAVE(Nome_tipo_aeronave);
ALTER TABLE INSTANCIA_TRECHO ADD FOREIGN KEY(Codigo_aeronave) REFERENCES AERONAVE(Codigo_aeronave);
ALTER TABLE INSTANCIA_TRECHO ADD FOREIGN KEY(Codigo_aeroporto_partida) REFERENCES AEROPORTO(Codigo_aeroporto);
ALTER TABLE INSTANCIA_TRECHO ADD FOREIGN KEY(Codigo_aeroporto_chegada) REFERENCES AEROPORTO(Codigo_aeroporto);
ALTER TABLE INSTANCIA_TRECHO ADD FOREIGN KEY(Numero_voo, Numero_trecho) REFERENCES TRECHO_VOO(Numero_voo, Numero_trecho);
ALTER TABLE PODE_POUSAR ADD FOREIGN KEY(Nome_tipo_aeronave) REFERENCES TIPO_AERONAVE(Nome_tipo_aeronave);
ALTER TABLE PODE_POUSAR ADD FOREIGN KEY(Codigo_aeroporto) REFERENCES AEROPORTO(Codigo_aeroporto);
ALTER TABLE TARIFA ADD FOREIGN KEY(Numero_voo) REFERENCES VOO(Numero_voo);
ALTER TABLE TRECHO_VOO ADD FOREIGN KEY(Codigo_aeroporto_partida) REFERENCES AEROPORTO(Codigo_aeroporto);
ALTER TABLE TRECHO_VOO ADD FOREIGN KEY(Codigo_aeroporto_chegada) REFERENCES AEROPORTO(Codigo_aeroporto);
ALTER TABLE TRECHO_VOO ADD FOREIGN KEY(Numero_voo) REFERENCES VOO(Numero_voo);
ALTER TABLE RESERVA_ASSENTO ADD FOREIGN KEY(Numero_voo,Numero_trecho, Data_reserva_assento) REFERENCES INSTANCIA_TRECHO(Numero_voo,Numero_trecho, Data_instancia_trecho);

insert into AEROPORTO values
	('1', 'Aeroporto Internacional do Recife', 'Recife', 'Pernambuco'),
    ('2', 'Aeroporto Internacional de São Paulo', 'São Paulo', 'São Paulo'),
    ('3', 'Aeroporto Internacional de Belo Horizonte', 'Belo Horizonte', 'Minas Gerais'),
    ('4','Aeroporto internacional Tom Jobim','Rio de Janeiro','Rio de Janeiro'),
    ('5','Aeroporto internacional de Santos Dumont','Rio de Janeiro','Rio de Janeiro'),
    ('6','Aeroporto de Vacaria','Vacaria','Rio Grande do Sul'),
    ('7','Aeroporto Internacional de Salvador','Salvador','Bahia'),
    ('8','Aeroporto de Paulo Afonso','Paulo Afonso','Bahia'),
    ('9','Aeroporto Senador Petrônio Portella','Teresina','Piauí');

insert into VOO values
	('1', 'Azul', 'Seg, Quar, Sex'),
    ('2', 'TAM', 'Ter, Qui, Sab'), 
    ('3', 'GOL', 'Seg, Quar, Sex'),
    ('4','TAP','Ter, Qui, Sab'),
	('5','American Airlines','Seg, Quar, Sex'),
    ('6','LATAM','Ter, Qui, Sab'),
    ('7','FLYWAY','Ter, Qui, Sab'),
    ('8','COMEFAST','Seg, Quar, Sex');
insert into TRECHO_VOO values
	('1','1','1','12:45','2','14:50'),
    ('2','2','2','12:50','1','14:55'),
    ('3','3','2','13:00','3','14:00'),
    ('4','4','1','08:00','2','10:15'),
    ('5','5','3','15:00','4','17:30'),
    ('6','6','2','19:00','3','21:10'),
    ('7','7','1','16:30','2','17:00'),
    ('8','8','3','11:45','4','13:05');
    
insert into TIPO_AERONAVE values
	('A319','60','TAM'),
    ('A321','60','TAM'),
    ('B767','60','AZUL'),
    ('A320 NEO','60','GOL'),
    ('ZFT23','45','TAP'),
    ('GTR34','30','LATAM'),
    ('ALLMIGHT','100','American Airlines'),
    ('BLACKCROW','60','FLYWAY'),
    ('JT244','45','COMEFAST');
    
insert into AERONAVE values
	('AV01','60','A319'),
    ('AV02','60','A321'),
    ('AV03','60','B767'),
    ('AV04','60','A320 NEO'),
    ('AV05','45','ZFT23'),
    ('AV06','30','GTR34'),
    ('AV07','100','ALLMIGHT'),
    ('AV08','60','BLACKCROW'),
    ('AV09','45','JT244');
    
insert into INSTANCIA_TRECHO values
    ('1',1,'2020-10-12','15','AV01','1','12:45','2','14:50'),
    ('2',2,'2021-02-05','7','AV02','2','12:50','1','14:55'),
    ('3',3,'2021-03-23','17','AV03','2','13:00','3','14:00'),
    ('4',4,'2021-04-11','40','AV05','1','08:00','2','10:15'),
    ('5',5,'2021-05-20','87','AV07','3','15:00','4','17:30'),
    ('6',6,'2021-05-24','23','AV06','2','19:00','3','21:10'),
    ('7',7,'2021-06-03','53','AV08','1','16:30','2','17:00'),
    ('8',8,'2021-06-30','39','AV09','3','11:45','4','13:05');
    
insert into TARIFA values
	('1',1,45,'restrição 01'),
    ('2',2,53,'restrição 02'),
    ('3',3,43,'restrição 03'),
    ('4',4,5,'restrição 04'),
    ('5',5,13,'restrição 05'),
    ('6',6,7,'restrição 06'),
    ('7',7,7,'restrição 07'),
    ('8',8,6,'restrição 08');

insert into PODE_POUSAR values
	('A319','1'),
    ('A321','1'),
    ('B767','2'),
    ('A320 NEO','2'),
    ('A319','3'),
    ('A321','3'),
    ('ZFT23','4'),
    ('GTR34','5'),
    ('ALLMIGHT','6'),
    ('BLACKCROW','7'),
    ('JT244','8'),
    ('GTR34','9'),
    ('ALLMIGHT','5'),
    ('BLACKCROW','1'),
    ('JT244','2'),
    ('A320 NEO','5'),
    ('A319','6'),
    ('A321','9'),
    ('ZFT23','5'),
    ('GTR34','1'),
    ('ALLMIGHT','2');

insert into RESERVA_ASSENTO values
	('1',1,'2020-10-12','12','João Kleber','8198987878'),
	('2',2,'2021-02-05','45','Maria Santos','8789566765'),
	('3',3,'2021-03-23','49','Roberto Machado','1232311212'),
	('1',1,'2020-10-12','29','Francisco Ferrari','8198956578'),
	('1',1,'2020-10-12','04','Jonas Martelo','7878687878'),
	('1',1,'2020-10-12','28','Gabriel Gabriela','9876789876'),
	('1',1,'2020-10-12','36','Giuseppe Paianno','4675825374'),
	('2',2,'2021-02-05','46','Neto Rocha','1234566765'),
	('2',2,'2021-02-05','15','Michael Tompson','8789567878'),
	('2',2,'2021-02-05','02','Rodrigo Rodriguez Ernandez','3219566765'),
	('3',3,'2021-03-23','19','Jerferson Andrade','3212311212'),
	('3',3,'2021-03-23','39','Linda Silva','5463311212'),
	('4',4,'2021-04-11','01','João Mateuz','87654321'),
	('4',4,'2021-04-11','11','Carla Noitez','87654322'),
	('4',4,'2021-04-11','23','Karlos Dias','87654555'),
	('5',5,'2021-05-20','01','Jonas Albuquerque','87656666'),
	('5',5,'2021-05-20','31','Joana Maria','87656622'),
	('5',5,'2021-05-20','11','Roberta Queiroz','87446666'),
	('5',5,'2021-05-20','10','Nando Reis','87656000'),
	('5',5,'2021-05-20','23','Cássia Eller','87654987'),
	('6',6,'2021-05-24','14','Matias Nascimento','87657863'),
	('6',6,'2021-05-24','15','Neto Machado','98765432'),
	('6',6,'2021-05-24','04','Julia Ferreira','87657321'),
	('6',6,'2021-05-24','12','Jackeline Santos','87657058'),
	('7',7,'2021-06-03','59','Daniel Cabrito','47657863'),
	('7',7,'2021-06-03','58','Daniela Rodriguez','47678986'),
	('7',7,'2021-06-03','19','Matias Cereja','47659872'),
	('7',7,'2021-06-03','10','Babu Maia','98987863'),
	('8',8,'2021-06-30','29','Israel Rodolffo','99997863'),
	('8',8,'2021-06-30','17','Eric Land','99990007'),
	('8',8,'2021-06-30','24','Rafael Carvalho','99997987'),
	('8',8,'2021-06-30','10','Lúcio Victor','67897863');

    
DELIMITER //

CREATE PROCEDURE TrechoVooPorAeroporto(
    IN Codigo_aero VARCHAR(5)
)
BEGIN
    SELECT *
     FROM TRECHO_VOO as TV
    WHERE TV.Codigo_aeroporto_partida = Codigo_aero or TV.Codigo_aeroporto_chegada = Codigo_aero;
END //

CREATE TRIGGER CriaTarifa AFTER INSERT ON VOO
FOR EACH ROW
BEGIN
    INSERT INTO TARIFA(Numero_voo, Codigo_tarifa) VALUES
    (NEW.Numero_voo, FLOOR(RAND()*10000));
END //

DELIMITER ;

COMMIT;
