# 💊 FDA Data Analytics Pipeline & AI Dashboard

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Manipulation-150458.svg)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)](https://streamlit.io/)

## 📌 Visão Geral do Projeto
Este projeto de portfólio demonstra a construção de um pipeline de dados ponta a ponta (ETL), focado em substituir processos manuais e fechamentos operacionais morosos por automação inteligente. 

O sistema consome dados abertos da base de medicamentos da **FDA (Food and Drug Administration)**, realiza a higienização utilizando processamento vetorizado, e consolida as informações em um Dashboard interativo integrado a um Agente de Inteligência Artificial (LLM) para extração de *insights* executivos.

---

## 🎯 Etapa do Projeto: Pitch Executivo (Data Analytics & Big Data)

Este repositório consolida a entrega técnica para a apresentação do *Pitch* executivo. A arquitetura foi desenhada para comprovar a transição de um problema operacional para uma solução orientada a dados (*Data-Driven*):

* **O Problema:** Ineficiência e falta de padronização na categorização de grandes volumes de dados regulatórios da indústria farmacêutica, dificultando a tomada de decisão rápida.
* **A Solução:** Implementação de um pipeline escalável em Python que extrai, traduz (Data Localization) e modela os dados, disponibilizando-os em uma interface visual de alto contraste e conectada a um LLM.
* **O Impacto:** Redução do tempo de análise de horas para segundos, garantindo governança (Data Quality) e acessibilidade da informação para a diretoria.

---

## 🏗️ Arquitetura de Dados e Decisões Técnicas

O projeto foi estruturado em três camadas independentes, garantindo resiliência e aderência às melhores práticas de Engenharia de Software (código limpo e PEP 8):

### 1. Camada Bronze (Ingestão de Dados)
* **Script:** `1_extracao.py`
* **Tecnologia:** Python (`requests`, `json`)
* **Decisão Arquitetônica (API vs. RPA):** A extração foi construída consumindo diretamente a API RESTful da FDA. Evitou-se ferramentas de automação de interface (*RPA*) de desktop como **PyAutoGUI** (frágil e monopoliza a máquina) ou *scrapers* web como **Selenium** e **Playwright** (focados em performance de navegação, mas desnecessários quando há *endpoints* públicos). A API garante resiliência e velocidade máxima na coleta do JSON bruto.

### 2. Camada Prata/Ouro (Transformação e Qualidade)
* **Script:** `2_tratamento_traduzido.py`
* **Tecnologia:** `Pandas`, `NumPy`
* **Processamento (Vetorização):** 
  * **Achatamento:** Uso do `pd.json_normalize()` para converter matrizes aninhadas em tabelas relacionais em milissegundos.
  * **Data Quality:** Remoção rigorosa de duplicatas e valores nulos (`dropna`, `drop_duplicates`) para manter a integridade referencial.
  * **Data Localization:** Aplicação do método vetorizado `.map()` e `.str.upper()` para traduzir variáveis e padronizar textos sem o uso de laços `for` lentos, entregando a base em português do Brasil.
* **Saída:** Geração de um arquivo `Base_Tratada_FDA.csv` limpo, formatado como uma verdadeira Tabela Fato.

### 3. Camada de Visualização (Business Intelligence)
* **Script:** `dash.py`
* **Tecnologia:** `Streamlit`, `Plotly Express`
* **Interface (UX/UI):** Dashboard responsivo utilizando `st.container(border=True)` para criar *Cards* de KPIs e gráficos iterativos, priorizando a escaneabilidade visual. O uso do `@st.cache_data` impede o recarregamento redundante da base.
* **Integração BI:** O formato tabular exportado atua como fonte universal. A mesma base que alimenta o Streamlit está perfeitamente modelada para ser importada no **Power BI** ou **Looker Studio**, pronta para a criação de um modelo em *Esquema Estrela (Star Schema)* sem necessidade de transformações pesadas em linguagem M ou DAX.

---

## 🤖 Integração com Inteligência Artificial
Para transcender a análise descritiva, o painel web possui um redirecionamento *Low-Code* nativo para o **NotebookLM**. O usuário é guiado a interagir com o Agente de IA para analisar anomalias nas proporções de fabricantes e gerar resumos textuais em linguagem natural.

---

## 🚀 Como Executar o Projeto Localmente

1. **Clone o repositório e instale as dependências:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
   cd SEU_REPOSITORIO
   pip install pandas plotly streamlit requests