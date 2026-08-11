import json
import requests

# O limite de 400 garante uma amostra sem sobrecarregar a memória.
URL_API_FDA = "https://api.fda.gov/drug/ndc.json?limit=400"
ARQUIVO_BRUTO = "data/raw/dados_brutos_fda.json"

def extrair_dados_api():
    """
    Atua como a camada de Ingestão do pipeline de dados.
    """
    print("📡 Iniciando conexão com a API da FDA...")
    
    # Web/APIs: O requests.get faz a comunicação direta via protocolo HTTP
    resposta = requests.get(URL_API_FDA)
    
    if resposta.status_code == 200:
        # Extrai apenasos dados que nos interessa 
        dados = resposta.json().get("results", [])
        
        # Salva o arquivo no disco 
        with open(ARQUIVO_BRUTO, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            
        print(f" Sucesso. {len(dados)} registros foram extraídos e salvos em '{ARQUIVO_BRUTO}'.")
    else:
        # Tratamento de erro básico caso o servidor da FDA caia
        print(f" Erro na integração. O servidor retornou o código HTTP: {resposta.status_code}")

if __name__ == "__main__":
    extrair_dados_api()