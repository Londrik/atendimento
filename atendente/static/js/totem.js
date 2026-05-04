let tipoSelecionado = "";

// Função para mostrar a tela de digitar o nome
function selecionarTipo(tipo) {
    tipoSelecionado = tipo;
    document.getElementById('grid-servicos').classList.add('hidden');
    document.getElementById('form-nome').classList.remove('hidden');
    document.getElementById('input-nome').focus();
    document.getElementById('titulo-totem').textContent = "Identifique-se";
}

// Função para VOLTAR para a tela de serviços
function voltar() {
    tipoSelecionado = "";
    document.getElementById('grid-servicos').classList.remove('hidden');
    document.getElementById('form-nome').classList.add('hidden');
    document.getElementById('input-nome').value = "";
    document.getElementById('titulo-totem').textContent = "Emissão de Senha";
}

async function gerarSenha() {
    const nome = document.getElementById('input-nome').value.trim();
    
    if (!nome) {
        alert("Por favor, digite seu nome.");
        return;
    }

    try {
        const response = await fetch('/gerar-senha', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                nome: nome, 
                tipo: tipoSelecionado 
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            alert(`✅ SENHA GERADA!\n\nNOME: ${nome}\nSENHA: ${data.codigo}\n\nAguarde no painel.`);
            voltar(); // Retorna automaticamente para o início após gerar
        } else {
            alert("❌ Erro ao gerar senha.");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("⚠️ Erro de conexão com o servidor.");
    }
}