import numpy as np
import pandas as pd
from pathlib import Path 
from estatisticas import calcular_estatisticas

dados = Path("dados/tratados/mulheres_escolaridade.csv")
indicador_completo = pd.read_csv(dados) #o arquivo que será lido
ufs_validas = [
    "Rondônia",
    "Acre",
    "Amazonas",
    "Roraima",
    "Pará",
    "Amapá",
    "Tocantins",
    "Maranhão",
    "Piauí",
    "Ceará",
    "Rio Grande do Norte",
    "Paraíba",
    "Pernambuco",
    "Alagoas",
    "Sergipe",
    "Bahia",
    "Minas Gerais",
    "Espírito Santo",
    "Rio de Janeiro",
    "São Paulo",
    "Paraná",
    "Santa Catarina",
    "Rio Grande do Sul",
    "Mato Grosso do Sul",
    "Mato Grosso",
    "Goiás",
    "Distrito Federal"
]

indicador_estados = indicador_completo.loc[
    indicador_completo["UF"].isin(ufs_validas) #valerá apenas se a unidade federativa estiver na lista de estados válidos
].copy() #essa função vai criar uma cópia do dataframe, para que as alterações feitas nele não afetem o dataframe original
indicador_brasil = indicador_completo.loc[
    indicador_completo["UF"] == "Brasil" #valerá apenas se a unidade federativa não estiver na lista de estados válidos
].copy() 
def df_estatisticas_por_ano(indicador_estados)-> pd.DataFrame:
    """
    Calcula estatísticas descritivas para cada ano no DataFrame.

    Parâmetros:
    indicador_estados (pd.DataFrame): DataFrame contendo os dados dos estados.

    Retorna:
    pd.DataFrame: DataFrame com as estatísticas calculadas para cada ano.
    """
    anos = indicador_estados["ano"].unique()  # Obtém os anos únicos no DataFrame
    estatisticas_por_ano = []

    for ano in anos:
        dados_ano = indicador_estados.loc[indicador_estados["ano"] == ano, "percentual_mulheres_superior_completo"] # Seleciona os dados do ano atual
        estatisticas = calcular_estatisticas(dados_ano) # chama a função calcular_estatisticas para calcular as estatísticas do ano atual
        registro = {"ano": ano, **estatisticas}  # Cria um registro com o ano e as estatísticas calculadas
        #o uso do **estatisticas vai desempacotar o dicionário de estatísticas e adicionar cada chave-valor ao registro
        #esse método se chama "desempacotamento de dicionário" e funciona ao adicionar cada chave-valor do dicionário como um par chave-valor no novo dicionário
        estatisticas_por_ano.append(registro)  # Adiciona o registro à lista
    return pd.DataFrame(estatisticas_por_ano)

def df_comparacao_2016_2025(indicador_estados):
    # Filtrar os dados originais (que estão em formato Long: uma linha por ano)
    dados = indicador_estados.loc[
        indicador_estados["ano"].isin([2016, 2025]),
        ["UF", "ano", "mulheres_superior_completo"]
    ].copy()
    
    # Passar temporariamente para WIDE para conseguir subtrair os anos
    df_wide = dados.pivot(
        index="UF", 
        columns="ano", 
        values="mulheres_superior_completo"
    ).reset_index()
    
    df_wide.columns.name = None
    df_wide = df_wide.rename(columns={2016: "2016", 2025: "2025"})
    
    # calcular a variação absoluta por estado
    df_wide["variacao_absoluta"] = df_wide["2025"] - df_wide["2016"]
    
    # Transformar de WIDE para LONG usando o .melt()
    comparacao_long = df_wide.melt(
        id_vars=["UF"],
        value_vars=["2016", "2025", "variacao_absoluta"],
        var_name="metrica",      # Nome da coluna que guardará "2016", "2025" ou "variacao_absoluta"
        value_name="quantidade"  # Nome da coluna que guardará os valores numéricos
    )
    
    return comparacao_long

def carregar_dados_dashboard(): #cria a função carregar_dados_dashboard para ler o arquivo CSV e retornar os DataFrames necessários para o dashboard
#Ao final, a função retorna um dicionário contendo os DataFrames necessários para o dashboard, incluindo o DataFrame completo do indicador, os dados do Brasil, os dados dos estados e o resumo das estatísticas por ano.
    caminho = Path(
        "dados/tratados/mulheres_escolaridade.csv"
    )

    # 1. Leitura do CSV
    indicador = pd.read_csv(caminho)

    # 2. Seleção dos dados nacionais
    dados_brasil = indicador.loc[
        indicador["UF"] == "Brasil"
    ].copy()

    dados_brasil = dados_brasil.sort_values(
        by="ano"
    )

    # 3. Seleção das 27 UFs
    indicador_estados = indicador.loc[
        indicador["UF"].isin(ufs_validas)
    ].copy()

    comparacao = df_comparacao_2016_2025(
        indicador_estados
    )

    # 4. Cálculo das estatísticas
    resumo = df_estatisticas_por_ano(
        indicador_estados
    ) 

    # 5. Entrega dos DataFrames
    return {
        "indicador": indicador,
        "dados_brasil": dados_brasil,
        "indicador_estados": indicador_estados,
        "resumo": resumo,
        "comparacao": comparacao
    }




"""
resumo = df_estatisticas_por_ano(indicador_estados) #chama a função df_estatisticas_por_ano para calcular as estatísticas do dataframe indicador_estados
print(resumo) #vai imprimir o dataframe resumo, que contém as estatísticas calculadas para cada ano

print("Quantidade de registros:")
print(indicador_estados.shape)

print("\nUFs distintas por ano:")
print(
    indicador_estados.groupby("ano")["UF"].nunique()
)

print("\nQuantidade de observações por ano:")
print(
    indicador_estados.groupby("ano").size()
)

print("\nValores numéricos disponíveis por ano:")
print(
    indicador_estados.groupby("ano")[
        "percentual_mulheres_superior_completo"
    ].count()
)

print("\nDuplicatas:")
print(
    indicador_estados.duplicated(
        subset=["UF", "ano"]
    ).sum()
)
"""