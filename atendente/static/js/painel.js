lucide.createIcons();
let ultimaSenha = ""; 

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
            const atual = fila[0];
            const guicheAtendimento = atual.guiche || "Guichê 01";

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

            historyList.innerHTML = fila.slice(1, 6).map(item => `
                <div class="flex justify-between items-center p-4 bg-gray-50 rounded-2xl border-l-8 border-senai">
                    <div class="flex flex-col">
                        <span class="text-4xl font-black text-senai">${item.codigo}</span>
                        <span class="text-xs font-bold text-gray-400 uppercase tracking-tighter">${item.guiche || 'Aguardando'}</span>
                    </div>
                    <span class="text-xl font-bold text-gray-500 uppercase">${item.nome.split(' ')[0]}</span>
                </div>
            `).join('');
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

setInterval(fetchFila, 3000);
fetchFila();