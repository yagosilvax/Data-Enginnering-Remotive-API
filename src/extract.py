import requests
import json
import os

class RemotiveExtractor:
    """Esta classe define os metódos para extrair os dados brutos da API do Remotive Jobs e retornar o arquivo JSON na pasta 'raw'. """

    def __init__(self,url="https://remotive.com/api/remote-jobs",output_path="raw/remotive_data.json"):
        self.url = url
        self.output_path = output_path

    def extrair_dados(self):
        """Método responsável pela requisição à API e por percorrer o objeto JSON"""
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            json_file = response.json()
            dados = json_file["jobs"]
            return dados
        except Exception:
            raise

    def salvar_dados(self,dados):
        """Método responsável por obter os dados brutos e salvá-los na pasta 'raw'"""
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path,'w') as file:
            json.dump(dados,file,indent=4)
        return self.output_path



