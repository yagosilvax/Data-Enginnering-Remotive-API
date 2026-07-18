CREATE TABLE dim_empresa(
id_empresa SERIAL PRIMARY KEY,
nome_empresa VARCHAR NOT NULL

)
CREATE TABLE dim_skill(
skill_id SERIAL PRIMARY KEY,
nome_skill VARCHAR NOT NULL



)
CREATE TABLE dim_categoria(

id_categoria SERIAL PRIMARY KEY,
nome_categoria VARCHAR NOT NULL



)
CREATE TABLE dim_local(
id_local SERIAL PRIMARY KEY,
localizacao_candidato VARCHAR NOT NULL

)

ALTER TABLE dim_empresa
ADD CONSTRAINT uq_empresa UNIQUE (nome_empresa)

ALTER TABLE dim_categoria
ADD CONSTRAINT uq_categoria UNIQUE (nome_categoria)

ALTER TABLE dim_skill
ADD CONSTRAINT uq_skill UNIQUE (nome_skill)]

ALTER TABLE dim_local
ADD CONSTRAINT uq_local UNIQUE (localizacao_candidato)


CREATE TABLE fato_vaga (
    vaga_id BIGINT PRIMARY KEY,

    empresa_id INT NOT NULL,
    categoria_id INT NOT NULL,
    localizacao_id INT NOT NULL,
	title VARCHAR(200),

    publication_date TIMESTAMP,

    salary_min NUMERIC,
    salary_max NUMERIC,
    currency VARCHAR(10),
    period VARCHAR(20),

    job_type VARCHAR(50),

    FOREIGN KEY (empresa_id)
        REFERENCES dim_empresa(id_empresa),

    FOREIGN KEY (categoria_id)
        REFERENCES dim_categoria(id_categoria),

    FOREIGN KEY (localizacao_id)
        REFERENCES dim_local(id_local)
);

ALTER TABLE fato_vaga
ADD CONSTRAINT uq_id_vaga UNIQUE(vaga_id)

SELECT * FROM fato_vaga