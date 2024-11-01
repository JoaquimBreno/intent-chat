import requests
import json
import os

def search_local(text_query):
    API_KEY = os.getenv('GOOGLE_API_KEY')
    if not API_KEY:
        raise ValueError("Chave da API do Google não encontrada. Certifique-se de que a variável de ambiente GOOGLE_API_KEY está configurada.")

    url = 'https://places.googleapis.com/v1/places:searchText'

    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.priceLevel,places.googleMapsUri,places.location',
    }

    data = {'textQuery': text_query}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na solicitação: {response.status_code}")

