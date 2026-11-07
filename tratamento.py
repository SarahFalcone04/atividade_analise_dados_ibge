from pathlib import Path
import pandas as pd

arquivo =Path("dados/brutos/tabela7189.csv")
#o arquivo que será lido

"""
Construção do dataframe e das linhas de anos e sexos, para que o pandas consiga ler o arquivo corretamente. 
O arquivo possui um cabeçalho com duas linhas, mas a segunda linha possui mais colunas do que a primeira. 
Isso pode causar problemas ao ler o arquivo, pois o pandas espera que todas as linhas do cabeçalho tenham o mesmo número de colunas. 
Para resolver esse problema, foram utilizados os métodos fillna e reindex para preencher os valores nulos e reorganizar os valores das linhas de anos e sexos, respectivamente.
"""
linha_anos = pd.read_csv(
    arquivo,
    sep=";", #o separador do arquivo
    header=None, #não vai usar nenhuma linha como cabeçalho
    skiprows=3, #vai pular as 3 primeiras linhas do arquivo para chegar na linha que possui os anos
    nrows=1, #vai ler apenas 1 linha do arquivo
    encoding="utf-8-sig",
    dtype=str #vai ler os dados como string, para evitar problemas com números que possuem vírgula
).iloc[0] #essa função vai pegar a primeira linha do dataframe, que é a linha que possui os anos

linha_sexos = pd.read_csv(
    arquivo, 
    sep= ";", 
    header=None,
    skiprows=4, #vai pular as 4 primeiras linhas do arquivo para chegar na linha que possui os sexos
    nrows=1,
    encoding="utf-8-sig",
    dtype=str
).iloc[0] #primeira linha do dataframe, que é a linha que possui os sexos

linha_anos = linha_anos.reindex( #o reindex vai reorganizar os valores da linha de anos para que fiquem na mesma ordem dos valores da linha de sexos
    range(len(linha_sexos)) #para cada valor da linha de sexos, ele vai pegar o valor correspondente da linha de anos
).ffill() #essa função vai preencher os valores nulos com o valor da célula anterior, para que todas as colunas tenham um ano associado

colunas = ["uf", "nivel_instrucao"]

for ano, sexo in zip(
    linha_anos.iloc[2:], #vai pegar todos os valores da linha de anos, exceto os dois primeiros, que são "uf" e "nivel_instrucao"
    linha_sexos.iloc[2:] #vai pegar todos os valores da linha de sexos, exceto os dois primeiros, que são "uf" e "nivel_instrucao"
):
    if str(ano).strip() != str(sexo).strip(): #se o ano for diferente do sexo, ele vai concatenar os dois valores com um underscore
        colunas.append(f"{str(ano).strip()}_{str(sexo).strip()}")
    else: #se forem iguais, ele vai usar apenas o ano como nome da coluna
        colunas.append(str(ano).strip())

df = pd.read_csv(
    arquivo, #o arquivo que será lido
    sep=";", #o separador do arquivo
    skiprows=5, #vai pular as 5 primeiras linhas do arquivo para chegar na linha que possui os dados
    header=None, #não vai usar nenhuma linha como cabeçalho
    names=colunas, #vai usar a lista de colunas que foi criada acima como cabeçalho
    encoding="utf-8-sig"
    )
"""
Aqui, o dataframe será mudado de wide para long, para que seja possível fazer análises mais facilmente.
"""
df_long = df.melt(
    id_vars=["uf", "nivel_instrucao"], #essas colunas não serão transformadas
    var_name="ano_e_sexo_do_indicador", #essa coluna vai receber os valores das colunas que foram transformadas
    value_name="pessoas" #essa coluna vai receber os valores das colunas que foram transformadas
)
"""
Construção das colunas de ano e sexo para análise
"""

separar_colunas = df_long["ano_e_sexo_do_indicador"].str.split("_", expand=True) #essa função vai separar os valores da coluna "ano_e_sexo_do_indicador" em duas colunas, usando o underscore como separador
# o uso do expand=True vai fazer com que a função retorne um dataframe com duas colunas, em vez de uma lista de listas

df_long["ano"] = separar_colunas[0].astype(int) #essa coluna vai receber os valores da primeira coluna criada pela função split e transformar os valores em inteiro, para que possam ser usados em análises numéricas
df_long["sexo"] = separar_colunas[1].str.casefold() #aqui, a coluna vai receber os valores da segunda coluna criada pela função split, e a função casefold vai transformar todos os valores em minúsculo para evitar problemas com letras maiúsculas e minúsculas
df_long["nivel_instrucao"] = df_long["nivel_instrucao"].str.casefold() #padronizar os valores

"""
Selecionando dados das mulheres para análise
"""
df_mulheres = df_long.loc[ #o loc vai selecionar apenas as linhas do dataframe que atendem a condição especificada
    df_long["sexo"]=="mulheres"
].copy() #essa função vai criar uma cópia do dataframe, para que as alterações feitas nele não afetem o dataframe original  

indicador = df_mulheres.pivot(
    index=["uf", "ano"],
    columns="nivel_instrucao", #essa coluna vai ser usada como cabeçalho
    values="pessoas" #essa coluna vai ser usada como valores do dataframe
).reset_index() #essa função vai transformar o índice do dataframe em uma coluna, para que possa ser usada em análises 

indicador = indicador.rename(
    columns={ #essa função vai renomear as colunas do dataframe, para que fiquem mais legíveis
    "uf": "UF",
    "total": "mulheres_25_mais",
    "superior completo": "mulheres_superior_completo"
    }
)

indicador["percentual_mulheres_superior_completo"] = (
    indicador["mulheres_superior_completo"] / indicador["mulheres_25_mais"] 
) * 100 #essa coluna mostrará o percentual de mulheres com ensino superior completo em relação ao total de mulheres com 25 anos ou mais

"""
Salvando os dados
"""
pasta = Path("dados/tratados")
pasta.mkdir(parents=True, exist_ok=True) #essa função vai criar a pasta "dados/tratados" caso ela não exista, e não vai gerar erro caso ela já exista

indicador.to_csv(
    pasta / "mulheres_escolaridade.csv", #o arquivo que será salvo
    index=False, #essa função vai salvar o arquivo sem o índice do dataframe
    encoding="utf-8-sig" 
)



"""
df = pd.read_csv(
   arquivo, #o arquivo que será lido
   sep=";", #o separador do arquivo
   skiprows=0,
   header=[3, 4], #as linhas que serão usadas como cabeçalho
   encoding="utf-8-sig"
)
df.columns = [ 
    f"{str(ano).strip()}_{str(sexo).strip()}" #se os nomes das colunas forem diferentes, ele vai concatenar o ano e o sexo com um underscore
    if str(ano).strip() != str(sexo).strip()
    else str(ano).strip() #se forem iguais, ele vai usar apenas o ano como nome da coluna
    for ano, sexo in df.columns #percorre todas as colunas do dataframe e aplica a lógica acima
] 
df.columns = df.columns.str.replace(r"_Unnamed:.*", "", regex=True) #para cada coluna que tiver "_Unnamed:" no nome, ele vai remover essa parte do nome da coluna

    Gerou erro: o header[3] possui 24 linhas, enquanto o header[4] possui 26 linhas. Isso significa que o arquivo CSV possui um cabeçalho com duas linhas, mas a segunda linha possui mais colunas do que a primeira. Isso pode causar problemas ao ler o arquivo, pois o pandas espera que todas as linhas do cabeçalho tenham o mesmo número de colunas.


""" 
