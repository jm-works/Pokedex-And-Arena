# Pokemon/app.py
from flask import Flask, render_template, jsonify, request
from src.api_client import fetch_pokemon_data
from src.formatters import processar_dados_para_exibicao
from src.battle_logic import simulate_battle

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/pokemon/<string:nome_ou_id>")
def get_pokemon(nome_ou_id):
    data_pokemon, data_species = fetch_pokemon_data(nome_ou_id)

    if not data_pokemon:
        return jsonify({"erro": f"Pokémon '{nome_ou_id}' não encontrado."}), 404

    dados_formatados = processar_dados_para_exibicao(data_pokemon, data_species)

    dados_formatados["raw_stats"] = data_pokemon["stats"]
    dados_formatados["sprites"] = data_pokemon["sprites"]
    dados_formatados["types"] = data_pokemon["types"]
    dados_formatados["moves"] = data_pokemon["moves"]

    return jsonify(dados_formatados)


@app.route("/battle")
def battle_page():
    """Serve a nova página da arena de batalha."""
    return render_template("battle.html")


@app.route("/api/battle/simulate", methods=["POST"])
def handle_battle_simulation():
    try:
        data = request.get_json()
        player_data = data.get("player")
        opponent_data = data.get("opponent")

        if not player_data or not opponent_data:
            return jsonify({"erro": "Dados do jogador ou oponente ausentes."}), 400

        log_completo, vencedor = simulate_battle(player_data, opponent_data)

        return jsonify({"log": log_completo, "winner": vencedor})

    except Exception as e:
        print(f"Erro na simulação de batalha: {e}")
        return jsonify({"erro": f"Erro interno do servidor: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
