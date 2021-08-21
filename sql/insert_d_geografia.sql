-- Table: analytics.d_geografia

CREATE TABLE IF NOT EXISTS analytics.d_geografia
(
    unidade_territorial_id integer NOT NULL,
    unidade_territorial character varying COLLATE pg_catalog."default" NOT NULL,
    nivel_territorial character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT d_geografia_pkey PRIMARY KEY (unidade_territorial_id)
)

COMMENT ON TABLE analytics.d_geografia
    IS 'Tabela de geografia para usar em Data Analytics com regiões em multiplos níveis (municipio, microrregiao, mesorregiao, regiao metropolitana, unidade da federação, grande região, país)';

COPY analytics.d_geografia
FROM '{source_filepath}'
DELIMITER ','
CSV HEADER;
