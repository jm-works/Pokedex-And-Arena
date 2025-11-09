import random

TYPE_CHART = {
    "normal": {"no_effect_to": ["ghost"], "not_very_effective_to": ["rock", "steel"]},
    "fire": {
        "not_very_effective_to": ["fire", "water", "rock", "dragon"],
        "super_effective_to": ["grass", "ice", "bug", "steel"],
    },
    "water": {
        "not_very_effective_to": ["water", "grass", "dragon"],
        "super_effective_to": ["fire", "ground", "rock"],
    },
    "electric": {
        "no_effect_to": ["ground"],
        "not_very_effective_to": ["electric", "grass", "dragon"],
        "super_effective_to": ["water", "flying"],
    },
    "grass": {
        "not_very_effective_to": [
            "fire",
            "grass",
            "poison",
            "flying",
            "bug",
            "dragon",
            "steel",
        ],
        "super_effective_to": ["water", "ground", "rock"],
    },
    "ice": {
        "not_very_effective_to": ["fire", "water", "ice", "steel"],
        "super_effective_to": ["grass", "ground", "flying", "dragon"],
    },
    "fighting": {
        "no_effect_to": ["ghost"],
        "not_very_effective_to": ["poison", "flying", "psychic", "bug", "fairy"],
        "super_effective_to": ["normal", "ice", "rock", "dark", "steel"],
    },
    "poison": {
        "no_effect_to": ["steel"],
        "not_very_effective_to": ["poison", "ground", "rock", "ghost"],
        "super_effective_to": ["grass", "fairy"],
    },
    "ground": {
        "no_effect_to": ["flying"],
        "not_very_effective_to": ["grass", "bug"],
        "super_effective_to": ["fire", "electric", "poison", "rock", "steel"],
    },
    "flying": {
        "not_very_effective_to": ["electric", "rock", "steel"],
        "super_effective_to": ["grass", "fighting", "bug"],
    },
    "psychic": {
        "no_effect_to": ["dark"],
        "not_very_effective_to": ["psychic", "steel"],
        "super_effective_to": ["fighting", "poison"],
    },
    "bug": {
        "not_very_effective_to": [
            "fire",
            "fighting",
            "poison",
            "flying",
            "ghost",
            "steel",
            "fairy",
        ],
        "super_effective_to": ["grass", "psychic", "dark"],
    },
    "rock": {
        "not_very_effective_to": ["fighting", "ground", "steel"],
        "super_effective_to": ["fire", "ice", "flying", "bug"],
    },
    "ghost": {
        "no_effect_to": ["normal"],
        "not_very_effective_to": ["dark"],
        "super_effective_to": ["psychic", "ghost"],
    },
    "dragon": {
        "not_very_effective_to": ["steel"],
        "super_effective_to": ["dragon"],
        "no_effect_to": ["fairy"],
    },
    "dark": {
        "not_very_effective_to": ["fighting", "dark", "fairy"],
        "super_effective_to": ["psychic", "ghost"],
    },
    "steel": {
        "not_very_effective_to": ["fire", "water", "electric", "steel", "fairy"],
        "super_effective_to": ["ice", "rock", "fairy"],
    },
    "fairy": {
        "not_very_effective_to": ["fire", "poison", "steel"],
        "super_effective_to": ["fighting", "dragon", "dark"],
    },
}


def _calculate_damage(attacker, defender, move):
    log = []

    if move["class"] == "physical":
        attacker_stat = attacker["attack"]
        defender_stat = defender["defense"]
    else:  # special
        attacker_stat = attacker["special_attack"]
        defender_stat = defender["special_defense"]

    effectiveness = 1
    move_type = move["type"]
    chart = TYPE_CHART.get(move_type, {})

    for def_type in defender["types"]:
        if def_type in chart.get("super_effective_to", []):
            effectiveness *= 2
        if def_type in chart.get("not_very_effective_to", []):
            effectiveness *= 0.5
        if def_type in chart.get("no_effect_to", []):
            effectiveness *= 0

    crit_multiplier = 1
    if random.random() < (1 / 16):
        log.append("Um acerto crítico!")
        crit_multiplier = 1.5

    damage = (move["power"] * (attacker_stat / defender_stat) / 5) + 2

    damage = max(
        1,
        round(damage * effectiveness * crit_multiplier * (random.uniform(0.85, 1.0))),
    )

    if effectiveness > 1:
        log.append("É super efetivo!")
    if 0 < effectiveness < 1:
        log.append("Não é muito efetivo...")
    if effectiveness == 0:
        log.append("Não teve efeito!")
        damage = 0

    return damage, log


def simulate_battle(fighter1, fighter2):

    log = [f"A batalha começa entre {fighter1['name']} e {fighter2['name']}!"]

    fighter1["currentHp"] = fighter1["maxHp"]
    fighter2["currentHp"] = fighter2["maxHp"]

    if fighter1["speed"] > fighter2["speed"]:
        attacker, defender = fighter1, fighter2
    elif fighter2["speed"] > fighter1["speed"]:
        attacker, defender = fighter2, fighter1
    else:
        log.append("As velocidades são idênticas! Sorteando quem começa...")
        attacker, defender = random.sample([fighter1, fighter2], 2)

    log.append(f"{attacker['name']} é mais rápido e ataca primeiro!")

    turn = 1
    while fighter1["currentHp"] > 0 and fighter2["currentHp"] > 0:
        log.append(f"--- Turno {turn} ---")

        move = random.choice(attacker["moves"])
        log.append(f"{attacker['name']} usa {move['name']}!")

        damage, effectiveness_log = _calculate_damage(attacker, defender, move)
        log.extend(effectiveness_log)

        defender["currentHp"] = max(0, defender["currentHp"] - damage)

        log.append(f"Causou {damage} de dano.")

        hp_log = f"{defender['name']} tem {defender['currentHp']}/{defender['maxHp']} HP restante."

        if defender is fighter1:
            log.append(f"[PLAYER_HP] {hp_log}")
        else:  # Só pode ser o fighter2
            log.append(f"[OPPONENT_HP] {hp_log}")

        if defender["currentHp"] <= 0:
            log.append(f"{defender['name']} desmaiou!")
            log.append(f"--- Fim da Batalha ---")
            log.append(f"O vencedor é {attacker['name']}!")
            return log, attacker["name"]

        attacker, defender = defender, attacker
        turn += 1

    return log, "Empate?"
