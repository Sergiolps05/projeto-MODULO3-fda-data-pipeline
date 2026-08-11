import json
import pandas as pd

ARQUIVO_ENTRADA = "data/raw/dados_brutos_fda.json"
ARQUIVO_SAIDA = "data/processed/Base_Tratada_FDA.csv"

def processar_dados_fda():
    """
    Pipeline de Tratamento: 
    Lê o JSON bruto, remove inconsistências (nulos e duplicatas),
    traduz o esquema e exporta uma Tabela Fato limpa.
    """
    print(" Carregando dados brutos para processamento...")
    
    try:
        with open(ARQUIVO_ENTRADA, 'r', encoding='utf-8') as f:
            dados_brutos = json.load(f)
    except FileNotFoundError:
        print(f" Erro: '{ARQUIVO_ENTRADA}' não encontrado.")
        return

    # ==========================================
    # 1. ACHATAMENTO E SELEÇÃO DE COLUNAS
    # ==========================================
    # Transforma o JSON aninhado em uma tabela plana
    df_completo = pd.json_normalize(dados_brutos)
    
    # Filtra apenas as colunas que nos interessam
    colunas_alvo = ['brand_name', 'generic_name', 'labeler_name', 'product_type']
    colunas_existentes = [col for col in colunas_alvo if col in df_completo.columns]
    
    df_limpo = df_completo[colunas_existentes].copy()
    
    # ==========================================
    # 2. HIGIENIZAÇÃO (Data Quality)
    # ==========================================
    # Salva o total inicial 
    linhas_antes = len(df_limpo)
    
    # A) Remoção de Duplicatas: 
    df_limpo.drop_duplicates(inplace=True)
    
    # B) Remoção de Nulos :
    df_limpo.dropna(subset=colunas_existentes, inplace=True)
    
    linhas_depois = len(df_limpo)
    print(f" Higienização: {linhas_antes - linhas_depois} registros defeituosos ou duplicados foram removidos.")

    # ==========================================
    # 3. TRADUÇÃO DAS COLUNAS 
    # ==========================================
    dicionario_colunas = {
        'brand_name': 'NOME_COMERCIAL',
        'generic_name': 'NOME_GENERICO',
        'labeler_name': 'FABRICANTE',
        'product_type': 'TIPO_PRODUTO'
    }
    df_limpo.rename(columns=dicionario_colunas, inplace=True)
    
    # ==========================================
    # 4. LIMPEZA VETORIZADA DE TEXTO
    # ==========================================
    if 'FABRICANTE' in df_limpo.columns:
        df_limpo['FABRICANTE'] = df_limpo['FABRICANTE'].str.upper().str.strip()
        
    if 'NOME_COMERCIAL' in df_limpo.columns:
        df_limpo['NOME_COMERCIAL'] = df_limpo['NOME_COMERCIAL'].str.upper().str.strip()

    # ==========================================
    # 5. TRADUÇÃO DOS DADOS 
    # ==========================================
    traducao_tipo = {
        'HUMAN PRESCRIPTION DRUG': 'MEDICAMENTO SOB PRESCRIÇÃO',
        'HUMAN OTC DRUG': 'MEDICAMENTO ISENTO DE PRESCRIÇÃO',
        'NON-STANDARDIZED ALLERGENIC': 'ALERGÊNICO NÃO PADRONIZADO'
    }
    
    if 'TIPO_PRODUTO' in df_limpo.columns:
        df_limpo['TIPO_PRODUTO'] = df_limpo['TIPO_PRODUTO'].map(traducao_tipo).fillna(df_limpo['TIPO_PRODUTO'])

    # ==========================================
    # 6. EXPORTAÇÃO
    # ==========================================
    df_limpo.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8')
    print(f" Base tratada e traduzida salva em '{ARQUIVO_SAIDA}'. Total Final: {linhas_depois} registros.")

if __name__ == "__main__":
    processar_dados_fda()