-- Table: analytics.bdd_municipio

CREATE TABLE IF NOT EXISTS analytics.bdd_municipio
(
    id_municipio integer NOT NULL,
    id_municipio_6 integer,
    id_municipio_tse integer,
    id_municipio_rf integer,
    id_municipio_bcb integer,
    nome character varying COLLATE pg_catalog."default",
    capital_uf boolean,
    id_comarca integer,
    id_regiao_saude integer,
    regiao_saude character varying COLLATE pg_catalog."default",
    id_regiao_imediata integer,
    regiao_imediata character varying COLLATE pg_catalog."default",
    id_regiao_intermediaria integer,
    regiao_intermediaria character varying COLLATE pg_catalog."default",
    id_microrregiao integer,
    microrregiao character varying COLLATE pg_catalog."default",
    id_mesorregiao integer,
    mesorregiao character varying COLLATE pg_catalog."default",
    ddd smallint,
    id_uf smallint,
    sigla_uf character varying(2) COLLATE pg_catalog."default",
    nome_uf character varying COLLATE pg_catalog."default",
    regiao character varying COLLATE pg_catalog."default",
    CONSTRAINT municipio_pkey PRIMARY KEY (id_municipio)
)

COMMENT ON TABLE analytics.municipio
    IS 'Fonte: basedosdados.org';

COPY analytics.municipio
FROM '{source_filepath}'
DELIMITER ','
CSV HEADER;
