from extract import extrair_dados

from transform import (
    trat_dados_origem,
    criar_dim_categoria,
    criar_dim_empresa,
    criar_dim_localizacao,
    criar_dim_skill
    
    

)
from transform import criar_fato,buscar_dimensoes
from load import carregar_fato_vagas
from load import carregar_dimensoes
import logging



logging.basicConfig(
    level = logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("vagas_remotas_pipeline.log"),
        logging.StreamHandler()
]

)
logger = logging.getLogger(__name__)


# Extração:
try:
    logger.info("============Extraindo dados...==============\n")
    data = extrair_dados()
    dados = data["jobs"]
    logger.info("Dados extraídos com sucesso!\n")
except Exception as e:
    logger.critical(f"Extração interrompida:{e}")


# Transformação:

try:
    logger.info("============Iniciando a transformação dos dados...==============")
    df_origem = trat_dados_origem(dados)

    dim_empresa = criar_dim_empresa(df_origem)

    df_exploded_skills = df_origem.explode("tags",ignore_index=True)

    dim_skill = criar_dim_skill(df_exploded_skills)
    dim_local = criar_dim_localizacao(df_origem)
    dim_categoria = criar_dim_categoria(df_origem)

    dimensoes = buscar_dimensoes()

    fato_vagas = criar_fato(df_origem,dimensoes)
    logger.info("Dados transformados e padronizados!\n")
except Exception as e:
    logger.error(f"Erro ao tentar transformar os dados: {e}")


# Carga dos dados:
try:
    logger.info("Iniciando a conexão com o o banco de dados...")
    tabelas_dim = {"dim_categoria":dim_categoria,
                "dim_empresa":dim_empresa,"dim_skill":dim_skill,
                "dim_local":dim_local}

    carregar_dimensoes(tabelas_dim)

    carregar_fato_vagas(fato_vagas,'fato_vaga')
    logger.info("Dados carregados no banco!\n")
except Exception as e:
    logger.info(f"Erro ao carregar os dados no banco:{e}")




