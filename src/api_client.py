import requests

BASE_URL = "https://pokeapi.co/api/v2"


def fetch_pokemon_data(nome_ou_id: str):

    nome_ou_id = nome_ou_id.lower()

    try:
        response_pokemon = requests.get(f"{BASE_URL}/pokemon/{nome_ou_id}")

        if response_pokemon.status_code == 404:
            print(f"Erro: Pokémon '{nome_ou_id}' não encontrado!")
            return None, None

        response_pokemon.raise_for_status()
        data_pokemon = response_pokemon.json()

        url_species = data_pokemon["species"]["url"]
        response_species = requests.get(url_species)
        response_species.raise_for_status()
        data_species = response_species.json()

        return data_pokemon, data_species

    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro de conexão: {e}")
        return None, None
    except Exception as e:
        print(f"Ocorreu um erro inesperado na API: {e}")
        return None, None
