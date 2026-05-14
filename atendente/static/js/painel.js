lucide.createIcons();
let ultimaSenha = ""; 

const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const socket = new WebSocket(`${protocol}//${window.location.host}/ws`);

socket.onmessage = function(event) {
    if (event.data === "atualizar_painel") {
        console.log("🔔 Nova senha chamada! Atualizando painel...");
        fetchFila();
    }
};

socket.onclose = function() {
    console.error("❌ Conexão perdida. Reconectando...");
    setTimeout(() => location.reload(), 5000);
};

// --- RELÓGIO ---
function updateClock() {
    const agora = new Date();
    document.getElementById('clock').textContent = agora.toLocaleTimeString('pt-BR');
    const opcoes = { weekday: 'long', day: 'numeric', month: 'long' };
    document.getElementById('date').textContent = agora.toLocaleDateString('pt-BR', opcoes);
}
setInterval(updateClock, 1000);
updateClock();

// --- ÁUDIO E VOZ ---
function tocarAlertaSonoro() {
    const audio = document.getElementById('audioChamada');
    if (audio) {
        audio.currentTime = 0; 
        audio.play().catch(e => console.log("Áudio bloqueado pelo navegador. Clique na tela."));
    }
}

function falarSenha(codigo, nome, guiche) {
    // Cancela qualquer fala que esteja rolando para não encavalar
    window.speechSynthesis.cancel(); 

    // Melhora a pronúncia: transforma "A001" em "A, zero, zero, um"
    const codigoSoletrado = codigo.split('').join(', ');
    const frase = `Senha: ${codigoSoletrado}. Aluno: ${nome}. Favor dirigir-se ao ${guiche}`;
    
    const mensagem = new SpeechSynthesisUtterance(frase);
    
    // Configurações da voz
    mensagem.lang = 'pt-BR';
    mensagem.rate = 0.85;  // Velocidade um pouco mais lenta (mais natural)
    mensagem.pitch = 1.0;  // Tom de voz normal
    
    window.speechSynthesis.speak(mensagem);
}

// --- LÓGICA DE FILA ---
async function fetchFila() {
    try {
        const response = await fetch('/listar-fila');
        const fila = await response.json();

        const ticketElement = document.getElementById('current-ticket');
        const nameElement = document.getElementById('current-name');
        const guicheElement = document.getElementById('current-guiche');
        const historyList = document.getElementById('history-list');

        if (fila && fila.length > 0) {
            const chamados = fila.filter(item => item.guiche !== null);
            
            if (chamados.length > 0) {
                const atual = chamados[0];
                const guicheAtendimento = atual.guiche;

                // SÓ CHAMA SE A SENHA MUDOU (Evita repetição infinita)
                if (atual.codigo !== ultimaSenha) {
                    ultimaSenha = atual.codigo;
                    
                    // 1º Toca o Plim-Plim
                    tocarAlertaSonoro();
                    
                    // 2º Espera 1.5 segundos e fala o nome (tempo do alerta sonoro acabar)
                    setTimeout(() => {
                        falarSenha(atual.codigo, atual.nome, guicheAtendimento);
                    }, 1500);
                    
                    // Efeito visual de destaque
                    document.body.classList.add('bg-yellow-400');
                    setTimeout(() => document.body.classList.remove('bg-yellow-400'), 1000);
                }

                ticketElement.textContent = atual.codigo;
                nameElement.textContent = atual.nome;
                guicheElement.textContent = guicheAtendimento;

                historyList.innerHTML = chamados.slice(1, 6).map(item => `
                    <div class="flex justify-between items-center p-4 bg-gray-50 rounded-2xl border-l-8 border-[#005ca9]">
                        <div class="flex flex-col">
                            <span class="text-4xl font-black text-[#005ca9]">${item.codigo}</span>
                            <span class="text-xs font-bold text-gray-400 uppercase">${item.guiche}</span>
                        </div>
                        <span class="text-xl font-bold text-gray-500 uppercase">${item.nome.split(' ')[0]}</span>
                    </div>
                `).join('');
            }
        } else {
            ticketElement.textContent = "---";
            nameElement.textContent = "SEM SENHAS";
            guicheElement.textContent = "---";
            historyList.innerHTML = '<p class="text-center text-gray-300 font-bold py-10">Fila vazia</p>';
        }
    } catch (error) {
        console.error("Erro ao buscar fila:", error);
    }
}

// OBRIGATÓRIO: O navegador só fala depois que você interage com a página.
document.addEventListener('click', () => {
    console.log("Sistema de áudio liberado!");
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(e => {});
    }
});

fetchFila();