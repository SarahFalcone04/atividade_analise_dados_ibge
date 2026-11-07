import tratamento as tr
from pathlib import Path
import csv

df = tr.df
print(df.head())

print(df.head()) #vai imprimir as 5 primeiras linhas do dataframe para verificar se os dados foram lidos corretamente
print(df.dtypes)
print(df.isna().sum()) #vai imprimir a quantidade de valores nulos em cada coluna do dataframe
print(tr.df_long.head(10)) #vai imprimir as 10 primeiras linhas do dataframe long para verificar se os dados foram transformados corretamente
print(tr.df_long['ano_e_sexo_do_indicador'].unique()) #vai imprimir os valores únicos da coluna "ano_e_sexo_do_indicador" para verificar se os dados foram transformados corretamente

dados = Path("dados/brutos/tabela100065")
with dados.open(
    "r",
    encoding="utf-8-sig",
    newline=""
) as f:
    leitor = csv.reader(f, delimiter=";")
    for indice, linha in enumerate(leitor, start=1):

        if indice <= 55:
            print(
                f"Linha {indice} | "
                f"Campos: {len(linha)} | "
                f"Conteúdo: {linha[:6]}"
            )