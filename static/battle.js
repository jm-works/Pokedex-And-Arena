document.addEventListener('DOMContentLoaded', () => {
    const p1_input = document.getElementById('p1-input');
    const p2_input = document.getElementById('p2-input');
    const battle_button = document.getElementById('battle-button');
    const battle_log = document.querySelector('.screen-log');

    const playerName = document.getElementById('player-name');
    const playerSprite = document.getElementById('player-sprite');
    const playerHpBar = document.getElementById('player-hp-bar');
    const playerHpText = document.getElementById('player-hp-text');
    const opponentName = document.getElementById('opponent-name');
    const opponentSprite = document.getElementById('opponent-sprite');
    const opponentHpBar = document.getElementById('opponent-hp-bar');
    const opponentHpText = document.getElementById('opponent-hp-text');

    let player = {};
    let opponent = {};

    battle_button.addEventListener('click', startBattle);
    battle_log.innerHTML = '';
    logMessage('Escolha os Pokémon para a batalha.');

    function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).replace(/-/g, ' ');
    }

    async function startBattle() {
        const name1 = p1_input.value.toLowerCase().trim();
        const name2 = p2_input.value.toLowerCase().trim();

        if (!name1 || !name2) {
            alert('Por favor, digite o nome dos dois Pokémon.');
            return;
        }

        battle_log.innerHTML = '';
        logMessage(`Buscando dados de ${name1} e ${name2}...`);
        battle_button.disabled = true; 

        try {
            const [data1, data2] = await Promise.all([
                fetch(`/api/pokemon/${name1}`).then(res => res.json()),
                fetch(`/api/pokemon/${name2}`).then(res => res.json())
            ]);

            if (data1.erro || data2.erro) {
                alert(`Erro: ${data1.erro || data2.erro}`);
                battle_button.disabled = false;
                return;
            }

            logMessage('Preparando os lutadores (buscando ataques...)');
            
            player = await createFighter(data1, playerName, playerSprite, playerHpBar, playerHpText, "player");
            opponent = await createFighter(data2, opponentName, opponentSprite, opponentHpBar, opponentHpText, "opponent");

            logMessage('Lutadores prontos!');

            const response = await fetch('/api/battle/simulate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ player: player, opponent: opponent })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.erro || "Erro desconhecido do servidor.");
            }

            const result = await response.json();
            
            await displayBattleLog(result.log);

        } catch (error) {
            console.error('Erro ao iniciar batalha:', error);
            logMessage(`Erro: ${error.message}. Tente novamente.`);
        } finally {
            battle_button.disabled = false; 
        }
    }

    async function createFighter(data, nameEl, spriteEl, hpBarEl, hpTextEl, side) {
        const stats = {};
        for (const stat of data.raw_stats) {
            stats[stat.stat.name] = stat.base_stat;
        }

        const learned_moves = [];
        const all_moves_urls = data.moves
            .map(m => m.move.url)
            .sort(() => 0.5 - Math.random());

        for (const url of all_moves_urls) {
            if (learned_moves.length >= 4) break;
            try {
                const move_data = await fetch(url).then(res => res.json());
                if (move_data.power && move_data.damage_class.name !== 'status') {
                    learned_moves.push({
                        name: capitalize(move_data.name),
                        power: move_data.power,
                        class: move_data.damage_class.name,
                        type: move_data.type.name
                    });
                }
            } catch (e) {}
        }
        
        if (learned_moves.length === 0) {
            learned_moves.push({ name: 'Tackle', power: 40, class: 'physical', type: 'normal' });
        }

        nameEl.textContent = data.nome;
        hpTextEl.textContent = `HP: ${stats.hp}/${stats.hp}`;
        hpBarEl.style.width = '100%';
        updateHealthBar(hpBarEl, 100);

        if (side === 'player') {
            spriteEl.src = data.sprites.back_default || data.sprite_url;
        } else {
            spriteEl.src = data.sprites.front_default || data.sprite_url;
        }
        
        return {
            name: data.nome,
            types: data.types.map(t => t.type.name), 
            maxHp: stats.hp,
            currentHp: stats.hp, 
            attack: stats.attack,
            defense: stats.defense,
            special_attack: stats['special-attack'], 
            special_defense: stats['special-defense'], 
            speed: stats.speed,
            moves: learned_moves,
        };
    }

    function updateHealthBar(hpBarEl, percent) {
        hpBarEl.classList.remove('low', 'critical');
        if (percent < 50) hpBarEl.classList.add('low');
        if (percent < 20) hpBarEl.classList.add('critical');
    }

    function logMessage(message) {
        const p = document.createElement('p');
        p.textContent = message;
        battle_log.appendChild(p);
        battle_log.scrollTop = battle_log.scrollHeight;
    }
    
    async function displayBattleLog(logLines) {
        battle_log.innerHTML = ''; 

        for (const line of logLines) {
            
            let message = line;

            if (line.startsWith("[PLAYER_HP]")) {
                message = line.replace("[PLAYER_HP] ", "");
                
                let matchPlayer = message.match(new RegExp(`${player.name} tem (\\d+)/(\\d+) HP`));
                if (matchPlayer) {
                    const currentHp = parseInt(matchPlayer[1]);
                    const maxHp = parseInt(matchPlayer[2]);
                    const percent = (currentHp / maxHp) * 100;
                    playerHpBar.style.width = `${percent}%`;
                    playerHpText.textContent = `HP: ${currentHp}/${maxHp}`;
                    updateHealthBar(playerHpBar, percent);
                    playerSprite.classList.add('hit');
                    setTimeout(() => playerSprite.classList.remove('hit'), 300);
                }

            } else if (line.startsWith("[OPPONENT_HP]")) {
                message = line.replace("[OPPONENT_HP] ", "");
                
                let matchOpponent = message.match(new RegExp(`${opponent.name} tem (\\d+)/(\\d+) HP`));
                if (matchOpponent) {
                    const currentHp = parseInt(matchOpponent[1]);
                    const maxHp = parseInt(matchOpponent[2]);
                    const percent = (currentHp / maxHp) * 100;
                    opponentHpBar.style.width = `${percent}%`;
                    opponentHpText.textContent = `HP: ${currentHp}/${maxHp}`;
                    updateHealthBar(opponentHpBar, percent);
                    opponentSprite.classList.add('hit');
                    setTimeout(() => opponentSprite.classList.remove('hit'), 300);
                }
            }
            
            logMessage(message);
            
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
});