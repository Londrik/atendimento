lucide.createIcons();
let ultimaSenha = ""; 

// --- CONFIGURAÇÃO DO WEBSOCKET ---
// Conecta ao servidor usando o protocolo ws:// ou wss://
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const socket = new WebSocket(`${protocol}//${window.location.host}/ws`);

socket.onmessage = function(event) {
    // Quando o main.py enviar "atualizar_painel", executamos a busca
    if (event.data === "atualizar_painel") {
        console.log("🔔 Nova senha chamada! Atualizando painel...");
        fetchFila();
    }
};

socket.onclose = function() {
    console.error("❌ Conexão com o servidor perdida. Tentando reconectar em 5s...");
    setTimeout(() => location.reload(), 5000);
};

// --- FUNÇÕES DE INTERFACE ---
function updateClock() {
    const agora = new Date();
    document.getElementById('clock').textContent = agora.toLocaleTimeString('pt-BR');
    const opcoes = { weekday: 'long', day: 'numeric', month: 'long' };
    document.getElementById('date').textContent = agora.toLocaleDateString('pt-BR', opcoes);
}

setInterval(updateClock, 1000);
updateClock();

function tocarAlertaSonoro() {
    const audio = document.getElementById('audioChamada');
    if (audio) {
        audio.currentTime = 0; 
        audio.play().catch(e => console.log("Aguardando interação para áudio:", e));
    }
}

function falarSenha(codigo, nome, guiche) {
    window.speechSynthesis.cancel(); 
    const codigoSoletrado = codigo.split('').join(' ');
    const texto = `Senha, ${codigoSoletrado}. ${nome}. Favor dirigir-se ao ${guiche}`;
    
    const mensagem = new SpeechSynthesisUtterance(texto);
    mensagem.lang = 'pt-BR';
    mensagem.rate = 0.9; 
    window.speechSynthesis.speak(mensagem);
}

async function fetchFila() {
    try {
        const response = await fetch('/listar-fila');
        const fila = await response.json();

        const ticketElement = document.getElementById('current-ticket');
        const nameElement = document.getElementById('current-name');
        const guicheElement = document.getElementById('current-guiche');
        const historyList = document.getElementById('history-list');

        if (fila && fila.length > 0) {
            // Filtramos apenas quem já tem guichê definido (foi chamado)
            const chamados = fila.filter(item => item.guiche !== null);
            
            if (chamados.length > 0) {
                const atual = chamados[0];
                const guicheAtendimento = atual.guiche;

                if (atual.codigo !== ultimaSenha) {
                    ultimaSenha = atual.codigo;
                    tocarAlertaSonoro();
                    
                    setTimeout(() => {
                        falarSenha(atual.codigo, atual.nome, guicheAtendimento);
                    }, 1200);
                    
                    document.body.classList.add('bg-yellow-400');
                    setTimeout(() => document.body.classList.remove('bg-yellow-400'), 1000);
                }

                ticketElement.textContent = atual.codigo;
                nameElement.textContent = atual.nome;
                guicheElement.textContent = guicheAtendimento;

                // Histórico: Pega do segundo ao sexto chamado
                historyList.innerHTML = chamados.slice(1, 6).map(item => `
                    <div class="flex justify-between items-center p-4 bg-gray-50 rounded-2xl border-l-8 border-senai">
                        <div class="flex flex-col">
                            <span class="text-4xl font-black text-senai">${item.codigo}</span>
                            <span class="text-xs font-bold text-gray-400 uppercase tracking-tighter">${item.guiche}</span>
                        </div>
                        <span class="text-xl font-bold text-gray-500 uppercase">${item.nome.split(' ')[0]}</span>
                    </div>
                `).join('');
            }
        } else {
            ticketElement.textContent = "---";
            nameElement.textContent = "SEM SENHAS";
            guicheElement.textContent = "---";
            historyList.innerHTML = '<p class="text-center text-gray-300 font-bold py-10 uppercase">Fila vazia</p>';
        }
    } catch (error) {
        console.error("Erro ao buscar fila:", error);
    }
}

// Ativa o modo tela cheia ao clicar em qualquer lugar do painel
document.addEventListener('click', () => {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    }
});

// Chamada inicial ao carregar a página
fetchFila();