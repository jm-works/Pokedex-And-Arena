import textwrap


def _formatar_stats(stats_json: list) -> str:
    stats_formatado = []
    for stat in stats_json:
        nome_stat = stat["stat"]["name"].capitalize()
        valor_stat = stat["base_stat"]
        stats_formatado.append(f"  - {nome_stat}: {valor_stat}")
    return "\n".join(stats_formatado)


def _formatar_habilidades(abilities_json: list) -> str:
    habilidades = []
    for ability in abilities_json:
        nome_habilidade = ability["ability"]["name"].capitalize()
        habilidades.append(nome_habilidade)
    return ", ".join(habilidades)


def _buscar_descricao_em_portugues(species_json: dict) -> str:
    for entry in species_json["flavor_text_entries"]:
        if entry["language"]["name"] == "pt":
            descricao_limpa = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            return descricao_limpa

    for entry in species_json["flavor_text_entries"]:
        if entry["language"]["name"] == "en":
            descricao_limpa = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            return f"(Descrição em Inglês) {descricao_limpa}"

    return "Descrição não encontrada."


def _formatar_evs(stats_json: list) -> str:
    evs = []
    for stat in stats_json:
        if stat["effort"] > 0:
            nome_stat = stat["stat"]["name"].capitalize()
            evs.append(f"{stat['effort']} {nome_stat}")

    if not evs:
        return "Nenhum"
    return ", ".join(evs)


def _formatar_gender(gender_rate: int) -> str:
    if gender_rate == -1:
        return "Sem gênero"

    taxa_femea = (gender_rate / 8) * 100
    taxa_macho = 100 - taxa_femea
    return f"{taxa_macho}% Macho, {taxa_femea}% Fêmea"


def processar_dados_para_exibicao(data_pokemon: dict, data_species: dict) -> dict:

    nome = data_pokemon["name"].capitalize()
    numero = data_pokemon["id"]
    tipos = ", ".join([t["type"]["name"].capitalize() for t in data_pokemon["types"]])
    stats = _formatar_stats(data_pokemon["stats"])
    habilidades = _formatar_habilidades(data_pokemon["abilities"])

    sprite_url = data_pokemon["sprites"]["other"]["official-artwork"]["front_default"]
    sprite_shiny_url = data_pokemon["sprites"]["other"]["official-artwork"][
        "front_shiny"
    ]

    if not sprite_url:
        sprite_url = data_pokemon["sprites"]["other"]["dream_world"]["front_default"]

    if not sprite_url:
        sprite_url = data_pokemon["sprites"]["front_default"]

    if not sprite_shiny_url:
        sprite_shiny_url = data_pokemon["sprites"]["front_shiny"]

    if not sprite_shiny_url:
        sprite_shiny_url = sprite_url

    descricao = _buscar_descricao_em_portugues(data_species)
    descricao_formatada = "\n".join(textwrap.wrap(descricao, width=60))

    taxa_crescimento = (
        data_species["growth_rate"]["name"].replace("-", " ").capitalize()
    )

    ev_yield = _formatar_evs(data_pokemon["stats"])

    taxa_captura = data_species["capture_rate"]
    grupos_ovo = ", ".join([g["name"].capitalize() for g in data_species["egg_groups"]])
    genero = _formatar_gender(data_species["gender_rate"])

    return {
        "nome": nome,
        "numero": numero,
        "tipos": tipos,
        "habilidades": habilidades,
        "stats": stats,
        "sprite_url": sprite_url,
        "sprite_shiny_url": sprite_shiny_url,  # Esta linha já existia
        "descricao": descricao_formatada,
        "growth_rate": taxa_crescimento,
        "ev_yield": ev_yield,
        "capture_rate": taxa_captura,
        "egg_groups": grupos_ovo,
        "gender_rate": genero,
    }
