import pandas as pd
import logging


from extract import extrair_dados
from transform import (
    trat_dados_origem,
    criar_dim_categoria,
    criar_dim_empresa,
    criar_dim_localizacao,
    criar_dim_skill
    
    

)
from transform import criar_fato,buscar_dimensoes,criar_bridge_skills
from load import carregar_fato_vagas
from load import carregar_dimensoes
from load import conectar_banco
from load import carregar_bridge_skill



logging.basicConfig(
    level = logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("vagas_remotas_pipeline.log"),
        logging.StreamHandler()
]

)
logger = logging.getLogger(__name__)


# Extração de todos os dados:

try:
    logger.info("===========INICIANDO PIPELINE E MODELAGEM DOS DADOS=============")
    try:
        logger.info("Extraindo dados...\n")
        data = extrair_dados()
        dados = data["jobs"]
        logger.info("Dados extraídos com sucesso!\n")
    except Exception as e:
        logger.critical(f"Extração interrompida:{e}")


    # Transformação geral dos dados de origem:
    try:
        logger.info("Iniciando a transformação dos dados de origem...")
        df_origem = trat_dados_origem(dados)
        df_exploded_skills = df_origem.explode("tags",ignore_index=True)
        logger.info("Dados transformados e padronizados!\n")
    except Exception as e:
        logger.error(f"Erro ao tentar transformar os dados: {e}")
        raise

    # Criação das tabelas de dimensão:
    try:
        logger.info("Criando tabelas de dimensão...")
        dim_empresa = criar_dim_empresa(df_origem)
        dim_skill = criar_dim_skill(df_exploded_skills)
        dim_local = criar_dim_localizacao(df_origem)
        dim_categoria = criar_dim_categoria(df_origem)
        logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas de dimensão:{e}")
        raise



    # Conexão com o banco de dados:
    try:
        logger.info("Iniciando conexão com o banco de dados...")
        engine = conectar_banco()
        if engine:
            logger.info("Conexão criada")
    except Exception as e:
        logger.critical(f"Erro ao tentar realizar conexão com o banco de dados:{e}")

    # Levando tabelas de dimensão para o banco:
    try:
        logger.info("Encaminhando as tabelas dimensionais para o banco de dados...")

        tabelas_dim = {"dim_categoria":dim_categoria,
                    "dim_empresa":dim_empresa,"dim_skill":dim_skill,
                    "dim_local":dim_local}

        carregar_dimensoes(tabelas_dim,engine)
        logger.info("Tabelas de dimensão enviadas para o banco de dados.")

    except Exception as e:
        logger.info(f"Erro ao enviar as tabelas para o banco de dados: {e}")



    # Consulta às tabelas de dimensão para criação da tabela de fatos:
    try:
        logger.info("Consultando tabelas de dimensão...")
        
        dimensoes = buscar_dimensoes(engine)

    # Criação da tabela de fatos:
        logger.info("Criando tabela de fatos...")
        fato_vagas = criar_fato(df_origem,dimensoes)

    # Levando a tabela de fatos para o banco:
        logger.info("Enviando tabela de fatos para o banco de dados...")
        carregar_fato_vagas(fato_vagas,'fato_vaga',engine)

    # Criação e envio da tabela de ponte entre as vagas e skills para relação * para muitos:
        logger.info("Criando tabela de ponte entre skills e vagas...")
        skill_banco = pd.read_sql("SELECT * FROM dim_skill", engine)
        dim_vaga_skill = criar_bridge_skills(df_exploded_skills,skill_banco)
        logger.info("Tabela criada e enviada para o banco.")
    except Exception as e:
        logger.error(f"Erro ao consultar as tabelas de dimensão e gerar a tabela de fatos:{e}")
        raise

    logger.info("==================PIPELINE FINALIZADO==================")

except: 
    logger.critical("Erro ao finalizar o pipeline")
    
        



