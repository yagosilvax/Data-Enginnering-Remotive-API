from sqlalchemy import create_engine,text
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def conectar_banco():
    """Realiza a conexão com o banco de dados."""
    host = os.getenv("host")
    database = os.getenv("database")
    user = os.getenv("usuario")
    port = os.getenv("port")
    password = os.getenv("senha_banco")
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(url)

    try:
        with engine.connect():
            return engine
    except Exception as e:
        raise


    
def carregar_dimensao(df,nome_tabela,conn):
        """Define o script SQL responsável por iterar as linhas de cada dataframe e inserir no banco de dados apenas registros novos."""

        coluna = df.columns[0]
        sql = f"""
        INSERT INTO {nome_tabela} ({coluna})
        VALUES (:valor)
        ON CONFLICT ({coluna}) DO NOTHING
        """
        for _, row in df.iterrows():
            conn.execute(
            text(sql),
            {"valor": row[coluna]}
        )


def carregar_dimensoes(tabelas_dim):
    """Carrega todas tabelas no banco de dados."""

    engine = conectar_banco()

    with engine.begin() as conn:
        for nome_tabela, df in tabelas_dim.items():
            carregar_dimensao(df, nome_tabela, conn)



def carregar_fato_vagas(tabela_fato,nome_tabela):
    """Carrega a tabela de fatos no banco de dados."""
    engine = conectar_banco()
    colunas = tabela_fato.columns.to_list()
    coluna_constraint = "vaga_id"
    colunas_sql = ", ".join(colunas)
    valores_sql = ", ".join([f":{col}" for col in colunas])

    with engine.begin() as conn:
        sql = f"""
        INSERT INTO {nome_tabela} ({colunas_sql})
        VALUES ({valores_sql})
        ON CONFLICT ({coluna_constraint}) DO NOTHING
        """
        for _, row in tabela_fato.iterrows():
            conn.execute(
            text(sql),
            row.to_dict()
        )

    
    
