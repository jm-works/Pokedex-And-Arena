document.addEventListener('DOMContentLoaded', () => {
    
    const searchButton = document.getElementById('search-button');
    const pokemonInput = document.getElementById('pokemon-input');
    const shinyButton = document.getElementById('shiny-button'); // Pega o novo botão

    const pokemonNameEl = document.getElementById('pokemon-name');
    const pokemonIdEl = document.getElementById('pokemon-id');
    const pokemonImageEl = document.getElementById('pokemon-image');
    const pokemonDescriptionEl = document.getElementById('pokemon-description');
    const pokemonTypesEl = document.getElementById('pokemon-types');
    const pokemonAbilitiesEl = document.getElementById('pokemon-abilities');
    const pokemonStatsEl = document.getElementById('pokemon-stats');

    const pokemonGrowthEl = document.getElementById('pokemon-growth');
    const pokemonCaptureEl = document.getElementById('pokemon-capture');
    const pokemonGenderEl = document.getElementById('pokemon-gender');
    const pokemonEggGroupsEl = document.getElementById('pokemon-egg-groups');
    const pokemonEvsEl = document.getElementById('pokemon-evs');

    let currentSpriteUrl = '';
    let shinySpriteUrl = '';
    let isShowingShiny = false;

    searchButton.addEventListener('click', () => {
        buscarPokemon();
    });

    pokemonInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            buscarPokemon();
        }
    });

    shinyButton.addEventListener('click', () => {
        if (isShowingShiny) {
            pokemonImageEl.src = currentSpriteUrl;
        } else {
            pokemonImageEl.src = shinySpriteUrl;
        }
        isShowingShiny = !isShowingShiny;
    });


    async function buscarPokemon() {
        const nomeOuId = pokemonInput.value.toLowerCase();
        if (!nomeOuId) return;

        pokemonNameEl.textContent = 'Buscando...';
        pokemonIdEl.textContent = '#???';

        try {
            const response = await fetch(`/api/pokemon/${nomeOuId}`);
            
            if (!response.ok) {
                const erro = await response.json();
                alert(erro.erro || 'Pokémon não encontrado!');
                resetarPokedex();
                return;
            }

            const data = await response.json();
            atualizarPokedex(data);

        } catch (error) {
            console.error('Erro ao buscar Pokémon:', error);
            alert('Falha ao conectar ao servidor. Verifique se o app.py está rodando.');
            resetarPokedex();
        }
    }

    function atualizarPokedex(data) {
        pokemonNameEl.textContent = data.nome;
        pokemonIdEl.textContent = `#${data.numero}`;
        
        currentSpriteUrl = data.sprite_url;
        shinySpriteUrl = data.sprite_shiny_url;
        
        pokemonImageEl.src = currentSpriteUrl;
        pokemonImageEl.alt = data.nome;
        isShowingShiny = false;
        
        if (currentSpriteUrl && shinySpriteUrl && currentSpriteUrl !== shinySpriteUrl) {
            shinyButton.style.display = 'block';
        } else {
            shinyButton.style.display = 'none';
        }

        pokemonDescriptionEl.textContent = data.descricao.replace(/(\r\n|\n|\r)/gm," ");
        pokemonTypesEl.textContent = data.tipos;
        pokemonAbilitiesEl.textContent = data.habilidades;
        
        pokemonStatsEl.innerHTML = '';
        data.stats.split('\n').forEach(stat => {
            const li = document.createElement('li');
            li.textContent = stat;
            pokemonStatsEl.appendChild(li);
        });

        pokemonGrowthEl.textContent = data.growth_rate;
        pokemonCaptureEl.textContent = data.capture_rate;
        pokemonGenderEl.textContent = data.gender_rate;
        pokemonEggGroupsEl.textContent = data.egg_groups;
        pokemonEvsEl.textContent = data.ev_yield;
    }

    function resetarPokedex() {
        pokemonNameEl.textContent = 'Pokédex';
        pokemonIdEl.textContent = '#???';
        pokemonImageEl.src = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/dream-world/132.svg";
        pokemonImageEl.alt = "Pokémon";
        pokemonDescriptionEl.textContent = "Digite o nome ou ID de um Pokémon e clique em 'Buscar'.";
        pokemonTypesEl.textContent = '---';
        pokemonAbilitiesEl.textContent = '---';
        pokemonStatsEl.innerHTML = '<li>- HP: ---</li><li>- Attack: ---</li><li>- Defense: ---</li>';

        pokemonGrowthEl.textContent = '---';
        pokemonCaptureEl.textContent = '---';
        pokemonGenderEl.textContent = '---';
        pokemonEggGroupsEl.textContent = '---';
        pokemonEvsEl.textContent = '---';

        shinyButton.style.display = 'none';
        currentSpriteUrl = '';
        shinySpriteUrl = '';
        isShowingShiny = false;
    }
});