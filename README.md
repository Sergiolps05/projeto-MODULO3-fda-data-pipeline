#  Projeto: FDA Data Analytics Pipeline & AI Dashboard
**Desenvolvido por:** Sérgio

##  O Tema e a Pergunta de Negócio
* **Tema:** Automação de extração e tratamento de dados regulatórios do setor farmacêutico para painéis de *Business Intelligence*.
* **A Pergunta:** Como podemos automatizar a extração, higienização e análise descritiva de dados da FDA para identificar a concentração de mercado e os fabricantes dominantes, sem a necessidade de intervenção manual em planilhas?

---

##  API Utilizada
A extração de dados (Camada Bronze) foi construída consumindo diretamente a API pública da FDA. Evitou-se o uso de ferramentas de RPA como PyAutoGUI ou Selenium, pois integrações via API RESTful garantem resiliência e velocidade máxima na coleta de dados estruturados.
* **Nome da API:** openFDA (National Drug Code Directory)
* **Documentação Oficial:** [https://open.fda.gov/apis/drug/ndc/](https://open.fda.gov/apis/drug/ndc/)
* **Como acessar:** A API possui *endpoints* públicos abertos. O projeto consome a rota GET `https://api.fda.gov/drug/ndc.json?limit=400` para extrair uma amostra validada, sem a necessidade de chaves de autenticação (API Keys).

---

##  A Base de Dados Gerada
O script de tratamento utiliza a vetorização nativa das bibliotecas **Pandas** e **NumPy** para achatar o JSON, remover inconsistências (nulos e duplicatas) e traduzir as informações de forma escalável. 
O resultado é a geração da tabela fato **`Base_Tratada_FDA.csv`**, estruturada nos padrões para criação de *Star Schema* (Esquema Estrela) no Power BI ou Looker. As principais colunas geradas são:
* `NOME_COMERCIAL`: Nome de mercado do medicamento (traduzido do original *brand_name*).
* `NOME_GENERICO`: Princípio ativo do medicamento (*generic_name*).
* `FABRICANTE`: Empresa responsável pela produção (*labeler_name*).
* `TIPO_PRODUTO`: Categoria regulatória do produto traduzida para o português, como "Medicamento sob Prescrição" ou "Medicamento Isento de Prescrição" (*product_type*).

---

##  Integração Low-Code (Agente de IA)
Para fornecer uma interface de análise prescritiva, a Tabela Fato foi integrada ao **NotebookLM** do Google (ferramenta Low-Code baseada em LLM). O Agente permite que gestores conversem com os dados estruturados em linguagem natural. 

**3 exemplos de perguntas que o agente responde ao vivo:**
1. *"Quais são as três categorias de produtos farmacêuticos mais frequentes nesta base e qual o volume de cada uma?"*
2. *"Liste os top 5 fabricantes com maior diversidade de medicamentos comerciais registrados."*
3. *"Faça um resumo executivo identificando se existe uma concentração de mercado (monopólio) em algum tipo específico de produto regulamentado."*

---

##  Instruções de Execução (Como rodar o projeto localmente)

Para garantir as boas práticas de desenvolvimento e evitar conflitos de versão no seu sistema, siga o passo a passo abaixo para executar o pipeline e o painel iterativo:

### 1. Criação do Ambiente Virtual (PEP 8 / Boas Práticas)
Abra o terminal na raiz do projeto e crie um ambiente virtual isolado. Em seguida, ative-o:

```bash
# Criação do ambiente virtual
python -m venv .venv

# Ativação no Windows (Terminal VS Code)
.venv\Scripts\activate

# Ativação no Linux/Mac
source .venv/bin/activate
```

### 2. Instalação das Bibliotecas Necessárias
Com o ambiente ativado (você verá `(.venv)` no terminal), instale as bibliotecas. Utilizamos **Pandas** e **NumPy** para processamento vetorizado em alta velocidade e **Streamlit** com **Plotly** para a renderização do Dashboard:

```bash
pip install pandas numpy plotly streamlit requests
```

### 3. Variáveis de Ambiente e Segurança
O projeto realiza requisições HTTP (`requests`) para os *endpoints* públicos da API da FDA. Como são dados governamentais abertos, **não há necessidade** de configurar um arquivo `.env` com tokens de acesso ou senhas. A conexão é direta e anônima.

### 4. Execução do Pipeline (ETL) e Interface
Execute os comandos abaixo sequencialmente na raiz do projeto:

**Passo A: Ingestão e Tratamento (Camada de Dados)**
```bash
# 1. Puxa os dados brutos (JSON) da API
python 1_extracao.py

# 2. Aplica limpeza vetorizada e exporta a Base_Tratada_FDA.csv
python 2_tratamento_traduzido.py
```

**Passo B: Visualização (Business Intelligence)**
```bash
# 3. Levanta o servidor local da interface web
streamlit run dash.py
```
*(O painel abrirá automaticamente no seu navegador padrão. A aplicação utiliza o decorador `@st.cache_data` do Streamlit para armazenar a leitura da base em cache, garantindo que as filtragens e os gráficos sejam atualizados instantaneamente sem reprocessar o CSV).*