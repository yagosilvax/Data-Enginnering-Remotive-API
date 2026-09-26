from sqlalchemy import create_engine,text
import os
from dotenv import load_dotenv

load_dotenv(override=True)


class EnviarBanco:
    """A classe EnviarBanco gerencia as conexões com o banco de dados e envia todas as tabelas de dimensão e fato para o data warehouse."""
    def __init__(self):
        self.engine = self._conectar()

    def _conectar(self):
        """Realiza a conexão com o banco de dados."""
        self.host = os.getenv("host")
        self.database = os.getenv("database")
        self.user = os.getenv("usuario")
        self.port = os.getenv("port")
        self.password = os.getenv("senha_banco")
        url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

        engine = create_engine(url)

        try:
            with engine.connect():
                return engine
        except Exception:
            raise


    def _executar_upsert(self,df,nome_tabela,conn,chave):
        colunas_df = df.columns.to_list()
        chave = [chave] if isinstance(chave,str) else list(chave)
        colunas_sql = ", ".join(colunas_df)
        valores_sql = ", ".join([f":{col}" for col in colunas_df])
        chave_sql = ", ".join(chave)
        colunas_update = [col for col in colunas_df if col not in chave]

        if colunas_update:
            set_sql = ", ".join([f"{col} = EXCLUDED.{col}" for col in colunas_update])
            constraint_sql = f"DO UPDATE SET {set_sql}"
        else:
            constraint_sql = "DO NOTHING"

        sql = f"""
            INSERT INTO {nome_tabela} ({colunas_sql})
            VALUES ({valores_sql})
            ON CONFLICT ({chave_sql}) {constraint_sql}
            """
        records = df.to_dict(orient="records")
        conn.execute(text(sql),records)


 
    def carregar_dimensoes(self,tabelas_dim: dict):
        """Este método é responsável por carregar todas tabelas de dimensão no banco de dados."""
        with self.engine.begin() as conn:
            for nome_tabela, df in tabelas_dim.items():
                coluna_chave = df.columns[0]
                self._executar_upsert(df, nome_tabela, conn,coluna_chave)



    def carregar_fato_vagas(self,tabela_fato,nome_tabela):
        """Este método é responsável por carregar a tabela de fatos no banco de dados."""
        with self.engine.begin() as conn:
            self._executar_upsert(tabela_fato,nome_tabela,conn,"vaga_id")

    
    def carregar_bridge_skill(self,df_bridge,nome_tabela):
        """Este método é responsável por carregar a tabela de ponte no banco de dados."""
        with self.engine.begin() as conn:
            self._executar_upsert(df_bridge,nome_tabela,conn,["vaga_id","skill_id"])
   
