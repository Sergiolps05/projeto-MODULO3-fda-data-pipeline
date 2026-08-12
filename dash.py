import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Painel FDA", layout="wide")

@st.cache_data
def carregar_dados() -> pd.DataFrame:
    return pd.read_csv("data/processed/Base_Tratada_FDA.csv")

def renderizar_painel():
    """Renderiza a interface do Dashboard."""
    st.title(" Painel Analítico FDA")
    
    # 1. BOTÃO DO AGENTE IA
    st.markdown("### 🤖 Assistente Virtual Integrado")
    st.write("Converse diretamente com os dados para obter resumos executivos.")
    url_agente = "https://notebook.google.com/notebook/a4e2976c-dac2-41a3-93cd-146ec65470fd"
    st.link_button("Abrir Agente Analítico", url_agente, type="primary")
    
    st.divider()
    
    df_completo = carregar_dados()
    
    # 2. FILTRO INTERATIVO
    st.subheader("Filtros Analíticos")
    lista_fabricantes = df_completo['FABRICANTE'].unique().tolist()
    lista_fabricantes.insert(0, "TODOS")
    
    fabricante_selecionado = st.selectbox("Selecione o Fabricante:", lista_fabricantes)
    
    if fabricante_selecionado == "TODOS":
        df_filtrado = df_completo
    else:
        df_filtrado = df_completo[df_completo['FABRICANTE'] == fabricante_selecionado]

    st.divider()

    # 3. CARDS DE MÉTRICAS NATIVOS
    st.subheader("Visão Geral")
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    
    # O border=True já cria o agrupamento visual seguro
    with col_kpi1:
        with st.container(border=True):
            st.metric(label="Total de Registros", value=len(df_filtrado))
            
    with col_kpi2:
        with st.container(border=True):
            st.metric(label="Total de Fabricantes", value=df_filtrado['FABRICANTE'].nunique())
            

    st.divider()

    # 4. GRÁFICOS
    col_barras, col_pizza = st.columns(2)

    with col_barras:
        with st.container(border=True):
            st.subheader("Top Fabricantes (Volume)")
            top_fabricantes = df_filtrado['FABRICANTE'].value_counts().head(10).reset_index()
            top_fabricantes.columns = ['Fabricante', 'Quantidade']
            
            fig_barras = px.bar(
                top_fabricantes, 
                x='Fabricante', 
                y='Quantidade',
                color_discrete_sequence=['#0083B8'],
                text_auto=True
            )
            # Removemos a transparência forçada para evitar conflitos de Dark Mode
            st.plotly_chart(fig_barras, use_container_width=True)

    with col_pizza:
        with st.container(border=True):
            st.subheader("Proporção de Prescrição")
            contagem_tipos = df_filtrado['TIPO_PRODUTO'].value_counts().reset_index()
            contagem_tipos.columns = ['Categoria', 'Quantidade']
            
            fig_pizza = px.pie(
                contagem_tipos, 
                values='Quantidade', 
                names='Categoria', 
                hole=0.4, 
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_pizza, use_container_width=True)

    st.divider()
    
    # 5. TABELA
    st.subheader("Tabela Fato (Dados Estruturados)")
    with st.container(border=True):
        st.dataframe(df_filtrado, use_container_width=True)

if __name__ == "__main__":
    renderizar_painel()