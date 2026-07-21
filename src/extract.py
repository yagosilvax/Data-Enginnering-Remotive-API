
import requests
import json

def extrair_dados():
    """Extrai os dados brutos da API do Remotive Jobs e retorna o arquivo JSON na pasta 'raw'. """
    url = "https://remotive.com/api/remote-jobs"
    try:
        response = requests.get(url)
        response.raise_for_status
        json_file = response.json()

        with open(r"raw/remotive_data.json",'w') as file:
            json.dump(json_file,file,indent=4)
            return json_file
    except Exception:
        raise