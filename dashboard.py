import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from formatacao import carregar_dados_dashboard

dados = carregar_dados_dashboard()


indicador = dados["indicador"]
dados_brasil = dados["dados_brasil"]
indicador_estados = dados["indicador_estados"]
resumo=dados["resumo"]
comparacao = dados["comparacao"]
variacao = dados["comparacao"]

dados_brasil = dados_brasil.sort_values(by="ano", ascending=True)


#Criando gráficos com matplotlib, seaborn e streamlit para exibir a evolução do percentual
#de mulheres com ensino superior completo no Brasil ao longo dos anos.
#O gráfico será uma linha que conecta os pontos representando o percentual 
#em cada ano, permitindo visualizar tendências e mudanças ao longo do tempo.


fig, ax = plt.subplots(figsize=(10, 5)) #usando o matplotlib para criar a figura e os eixos do gráfico

ax.plot( #cria o gráfico de linha usando os dados do DataFrame, com marcadores nos pontos de dados e uma linha conectando-os
    dados_brasil["ano"],
    dados_brasil["percentual_mulheres_superior_completo"],
    marker="o",
    linewidth=2,
    label="Mulheres",
)
#outras opções de gráficos são:
#ax.bar() #gráfico de barras
#ax.scatter() #gráfico de dispersão
#ax.fill_between() #gráfico de área
#ax.pie() #gráfico de pizza
ax.set_title(
    "Evolução do Percentual de Mulheres com Ensino Superior Completo no Brasil", fontsize=14
)

ax.set_xlabel("Ano", fontsize=12)#nomeando o eixo x
ax.set_ylabel("Mulheres com Ensino Superior Completo (%)", fontsize=12) #nomeando o eixo y

ax.legend()#apresenta a legenda

fig.tight_layout()#ajusta o layout da figura para evitar sobreposição de elementos

st.pyplot(fig)

#construindo um bloxplot usando o seaborn

fig, ax=plt.subplots(figsize=(11, 6)) #usando o matplotlib para criar a figura e os eixos do gráfico
sns.boxplot(
    data=indicador_estados, #especifica o DataFrame que será usado para criar o boxplot
    x="ano", #definição eixo x
    y="percentual_mulheres_superior_completo", #definição eixo y
    ax=ax, #especifica os eixos do gráfico, ax=ax, para que o boxplot seja desenhado no eixo correto
    palette="Set3",
    whis=1.5, #define o comprimento dos bigodes do boxplot
    showfliers=True, #define se os outliers serão mostrados ou não
)
ax.set_title(
    "Distribuição da escolaridade superior feminina entre as UFs"
)

ax.set_xlabel("Ano")
ax.set_ylabel("Mulheres com Ensino Superior completo (%)")

ax.grid(axis="y", alpha=0.3) 
fig.tight_layout()
st.pyplot(fig)

#usando o plotly
fig_comparacao = px.bar(
    comparacao,
    x="quantidade",
    y="UF",
    color="metrica",
    barmode="group",
    orientation="h",
    category_orders={
        "metrica": ["2016", "2025"]
    },
    title="Mulheres com Ensino Superior Completo por UF",
    labels={
        "quantidade": "Quantidade (mil pessoas)",
        "metrica": "Ano",
        "UF": "Unidade da Federação"
    }
)

fig_comparacao.update_layout(
    height=850
)

st.plotly_chart(
    fig_comparacao,
    width="stretch"
)

fig_variacao = px.bar(
    variacao.sort_values(
        "quantidade",
        ascending=True
    ),
    x="quantidade",
    y="UF",
    orientation="h",
    title="Variação da Quantidade de Mulheres com Ensino Superior Completo (2016–2025)",
    labels={
        "quantidade": "Variação (mil pessoas)",
        "UF": "Unidade da Federação"
    }
)

fig_variacao.add_vline(
    x=0,
    line_dash="dash"
)

fig_variacao.update_layout(
    height=850
)

st.plotly_chart(
    fig_variacao,
    width="stretch"
)