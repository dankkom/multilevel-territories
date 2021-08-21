-- Table: analytics.ibge_rm_ride

CREATE TABLE IF NOT EXISTS analytics.ibge_rm_ride
(
    grande_reg character varying COLLATE pg_catalog."default",
    cod_uf smallint,
    sigla_uf character varying(2) COLLATE pg_catalog."default",
    cod integer,
    nome character varying COLLATE pg_catalog."default",
    tipo character varying COLLATE pg_catalog."default",
    cod_cat_assoc integer,
    cat_assoc character varying COLLATE pg_catalog."default",
    cod_mun integer,
    nome_mun character varying COLLATE pg_catalog."default",
    leg character varying COLLATE pg_catalog."default",
    data date
)

COMMENT ON TABLE analytics.ibge_rm_ride
    IS 'Fonte: IBGE';


COPY analytics.ibge_rm_ride
FROM '{source_filepath}'
DELIMITER ','
CSV HEADER;
