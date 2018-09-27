# Я скачал postgresql, так как прочел, что она из самых популярных СУБД
# и ее часто используют с python. Я пока не совсем понял, как это все работает
# я создал юзера, learn_python3 с паролем 123 (возможно он не понадобится, но пока хз), создал базу данных, в ней есть таблица,
# в которой я записал все поля, что были в постановке, поле дата-время объявления я разбил на 2 поля,
# поскольку не понял, какой тип ставить всему этому делу. Добавил такую вещь как sequence чтобы при добавлении
# данных генирировался внутренний id, если это действительно так работает.

CREATE USER learn_python3 WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD 'xxxxxx';

CREATE DATABASE avito_clon_db
    WITH 
    OWNER = learn_python3
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

CREATE SEQUENCE public.avito_clon_ids_seq;

ALTER SEQUENCE public.avito_clon_ids_seq
    OWNER TO learn_python3;

CREATE TABLE public.goods
(
    id integer NOT NULL DEFAULT nextval('avito_clon_ids_seq'::regclass),
    name text NOT NULL,
    avito_ad_number integer NOT NULL,
    avito_date_publication date NOT NULL,
    avito_time_publication time without time zone NOT NULL,
    photo_link text,
    adress text NOT NULL,
    price integer NOT NULL,
    ad_text text,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE public.goods
    OWNER to learn_python3;