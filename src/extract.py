
import requests
import json

def extrair_dados():
    url = "https://remotive.com/api/remote-jobs"
    try:
        response = requests.get(url)
        response.raise_for_status
        json_file = response.json()

        with open(r"raw/remotive_data.json",'w') as file:
            json.dump(json_file,file,indent=4)
            return json_file
    except Exception as e:
        print(f'Erro ao buscar os dados:{e}')