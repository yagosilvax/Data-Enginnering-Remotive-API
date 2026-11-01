from airflow.sdk import DAG, task
from datetime import datetime,timedelta

with DAG(
    dag_id="remotive_etl",
    default_args={"depends_on_past": False,
     "retries":1,
     "retry_delay": timedelta(minutes=5),
     },
    schedule="@daily",
    start_date=datetime(2026, 10, 25),
    description="ETL completo que extrai dados da Remotive API, transforma os dados e modela em um dw Postgres",
    catchup=False
) as dag:

    @task
    def extrair():
        from src.extract import RemotiveExtractor
        extrator = RemotiveExtractor()
        dados = extrator.extrair_dados()
        return extrator.salvar_dados(dados)

    @task
    def carregar_dimensoes(caminho_raw):
        import json
        from src.transform import TransformarDados
        from src.load import EnviarBanco

        with open(caminho_raw, encoding="utf-8") as f:
            dados = json.load(f)

        db = EnviarBanco()
        t = TransformarDados(dados, db.engine)
        t.trat_dados_origem()
        t.explodir_skills()

        db.carregar_dimensoes({
            "dim_empresa": t.criar_dim_empresa(),
            "dim_skill": t.criar_dim_skill(),
            "dim_categoria": t.criar_dim_categoria(),
            "dim_local": t.criar_dim_localizacao(),
        })
        return caminho_raw


    @task
    def carregar_fatos(caminho_raw):
        import json
        from src.transform import TransformarDados
        from src.load import EnviarBanco

        with open(caminho_raw, encoding="utf-8") as f:
            dados = json.load(f)

        db = EnviarBanco()
        t = TransformarDados(dados, db.engine)
        t.trat_dados_origem()
        t.explodir_skills()

        dimensoes = t.buscar_dimensoes()
        fato = t.criar_fato(dimensoes)
        bridge = t.criar_bridge_skills(dimensoes["dim_skill"])

        db.carregar_fato_vagas(fato, "fato_vaga")
        db.carregar_bridge_skill(bridge, "dim_vaga_skill") 


    raw = extrair()
    dims = carregar_dimensoes(raw)
    carregar_fatos(dims)

            
        



