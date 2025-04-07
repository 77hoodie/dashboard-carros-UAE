import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Dashboard")
st.text("Análise de carros usados nos Emirados Árabes Unidos")

df = pd.read_csv("dateassets/uae_used_cars_10k.csv")

# Limpeza de valores nulos
df = df.dropna(subset=["Price", "Mileage", "Make", "Year", "Body Type"])

# Coluna nova para fins de análise
df["price_per_km"] = df["Price"] / df["Mileage"].replace(0, 1)

# Filtros
with st.sidebar:
    st.header("Filtros")
    marcas = st.multiselect("Marca", options=df["Make"].unique(), default=None)
    tipos = st.multiselect("Tipo de carroceria", options=df["Body Type"].unique(), default=None)
    anos = st.slider("Ano de fabricação", int(df["Year"].min()), int(df["Year"].max()), (2012, 2023))
    preco_min, preco_max = st.slider("Faixa de preço (AED)", float(df["Price"].min()), float(df["Price"].max()), (float(df["Price"].min()), float(df["Price"].max())))

df_filtrado = df.copy()
if marcas:
    df_filtrado = df_filtrado[df_filtrado["Make"].isin(marcas)]
if tipos:
    df_filtrado = df_filtrado[df_filtrado["Body Type"].isin(tipos)]

df_filtrado = df_filtrado[(df_filtrado["Year"] >= anos[0]) & (df_filtrado["Year"] <= anos[1])]    
df_filtrado = df_filtrado[(df_filtrado["Price"] >= preco_min) & (df_filtrado["Price"] <= preco_max)]

tab1, tab2 = st.tabs(["Por filtro", "Geral"])

with tab1:
    # Gráfico de preço vs quilometragem
    fig1 = px.scatter(df_filtrado, x="Mileage", y="Price", color="Body Type", hover_data=["Make", "Model", "Year"], title="Preço em relação à quilometragem do carro")
    fig1.update_layout(height=400)

    # Gráfico de preço por tipo de carroceria
    fig2 = px.box(df_filtrado, x="Body Type", y="Price", color="Body Type", title="Distribuição de preços por tipo de carroceria")
    fig2.update_layout(height=400)

    # Gráfico de distribuição dos anos
    fig3 = px.histogram(df_filtrado, x="Year", nbins=20, title="Distribuição por ano de fabricação")
    fig3.update_layout(height=300)

    # Gráfico de preço médio por tipo de transmissão
    preco_medio = df_filtrado.groupby('Transmission')['Price'].mean().sort_values(ascending=False).reset_index()
    fig4 = px.pie(preco_medio, names='Transmission', values='Price', title='Distribuição do preço médio por tipo de transmissão')
    fig4.update_traces(textposition='inside', textinfo='percent+label')

    # Gráfico de preço médio por ano de fabricação
    preco_ano = df_filtrado.groupby("Year")["Price"].mean().reset_index()
    fig8 = px.line(preco_ano, x="Year", y="Price", title="Preço médio por ano de fabricação")
    fig8.update_layout(height=400)

    # Layout
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)

    st.plotly_chart(fig8, use_container_width=True)

    # Tabela de melhores preços por km rodado
    st.subheader("Carros mais baratos em relação ao km rodado")
    top_ofertas = df_filtrado.sort_values(by="price_per_km").head(10)
    st.dataframe(top_ofertas[["Make", "Model", "Year", "Price", "Mileage", "price_per_km"]])

    # Tabela de modelos mais comuns da marca filtrada
    if len(marcas) == 1:
        st.subheader(f"Modelos mais comuns da marca {marcas[0]}")
        modelos_top = df_filtrado["Model"].value_counts().head(10).reset_index()
        modelos_top.columns = ["Model", "Count"]
        st.dataframe(modelos_top)

with tab2:
    
    st.subheader("Não selecione filtros, pois a análise é geral")

    # Gráfico de preço médio por marca
    preco_medio = df_filtrado.groupby('Make')['Price'].mean().sort_values(ascending=False).reset_index()
    fig4 = px.bar(preco_medio, x='Make', y='Price', title='Preço médio por marca', labels={'Price': 'Preço médio', 'Make': 'Marca'})
    fig4.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

    # Gráfico de número de veículos por marca
    contagem_marcas = df_filtrado['Make'].value_counts().reset_index()
    contagem_marcas.columns = ['Make', 'Count']
    fig5 = px.bar(contagem_marcas, x='Make', y='Count',title='Quantidade de veículos por marca', labels={'Count': 'Quantidade', 'Make': 'Marca'})
    fig5.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig5, use_container_width=True)

    # Gráfico de preço por quilometragem por marca
    preco_km_marca = df_filtrado.groupby('Make')['price_per_km'].mean().sort_values(ascending=False).reset_index()
    fig6 = px.bar(preco_km_marca, x='Make', y='price_per_km', title='Relação preço por quilometragem por marca', labels={'price_per_km': 'Preço por km', 'Make': 'Marca'})
    fig6.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig6, use_container_width=True)
    
    # Gráfico de preço médio por tipo de carroceria
    preco_medio_carroceria = df_filtrado.groupby("Body Type")["Price"].mean().sort_values(ascending=False).reset_index()
    fig7 = px.bar(preco_medio_carroceria, x="Body Type", y="Price", color="Body Type", title="Preço médio por tipo de carroceria", labels={"Price": "Preço médio", "Body Type": "Tipo de carroceria"})
    fig7.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig7, use_container_width=True)