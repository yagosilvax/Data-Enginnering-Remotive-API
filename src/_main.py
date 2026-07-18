from extract import extrair_dados

from transform import (
    trat_dados_origem,
    criar_dim_categoria,
    criar_dim_empresa,
    criar_dim_localizacao,
    criar_dim_skill


)
from load import carregar_dimensoes

# Extração:

data = extrair_dados()

dados = data["jobs"]

# Transformação:
df_origem = trat_dados_origem(dados)

dim_empresa = criar_dim_empresa(df_origem)

df_exploded_skills = df_origem.explode("tags",ignore_index=True)

dim_skill = criar_dim_skill(df_exploded_skills)
dim_local = criar_dim_localizacao(df_origem)
dim_categoria = criar_dim_categoria(df_origem)

# Carga dos dados:

tabelas_dim = {"dim_categoria":dim_categoria,
               "dim_empresa":dim_empresa,"dim_skill":dim_skill,
               "dim_local":dim_local}

carregar_dimensoes(tabelas_dim)
