lucide.createIcons();
let atendimentoAtual = null;

async function chamarProximo() {
    const guicheSelecionado = document.getElementById("select-guiche").value;
    
    try {
        const response = await fetch("/chamar-proxima", { 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ guiche: guicheSelecionado })
        });

        if (response.ok) {
            atendimentoAtual = await response.json();
            document.getElementById("atendente-codigo").textContent = atendimentoAtual.codigo;
            document.getElementById("atendente-nome").textContent = atendimentoAtual.nome;
            atualizarFila();
        } else {
            const erroData = await response.json();
            alert("Atenção: " + (erroData.detail || "Fila vazia ou erro no servidor"));
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro ao conectar com o servidor.");
    }
}

async function chamarNovamente() {
    if (!atendimentoAtual) return alert("Nenhuma senha foi chamada ainda.");
    alert(`Repetindo chamada: ${atendimentoAtual.codigo} no ${atendimentoAtual.guiche}`);
}

async function atualizarFila() {
    try {
        const response = await fetch("/listar-fila");
        const fila = await response.json();
        
        const lista = document.getElementById("lista-espera");
        const contador = document.getElementById("contador-fila");
        
        contador.textContent = `${fila.length} na fila`;

        if (fila.length === 0) {
            lista.innerHTML = `<p class="text-center text-gray-400 py-4">Ninguém aguardando.</p>`;
            return;
        }

        lista.innerHTML = fila.map(item => `
            <div class="flex justify-between items-center p-4 bg-gray-50 rounded-xl border-l-4 ${item.tipo === "Prioritário" || item.tipo === "Preferencial" ? "border-red-500" : "border-senai"}">
                <div>
                    <span class="font-black text-lg">${item.codigo}</span>
                    <span class="ml-3 text-gray-600 font-medium">${item.nome}</span>
                </div>
                <span class="text-xs font-bold uppercase px-2 py-1 rounded ${item.tipo === "Prioritário" || item.tipo === "Preferencial" ? "bg-red-100 text-red-600" : "bg-blue-100 text-blue-600"}">
                    ${item.tipo}
                </span>
            </div>
        `).join("");
    } catch (error) {
        console.error("Erro ao atualizar fila:", error);
    }
}

setInterval(atualizarFila, 5000);
atualizarFila();