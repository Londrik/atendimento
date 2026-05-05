async function gerarSenha(tipo) {
    const nomePadrao = "Aluno SENAI"; 

    try {
        const response = await fetch('/gerar-senha', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                nome: nomePadrao, 
                tipo: tipo 
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            exibirSucesso(data.codigo, tipo);
        } else {
            alert("❌ Erro ao gerar senha.");
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("⚠️ Erro de conexão com o servidor.");
    }
}

function exibirSucesso(codigo, tipo) {
    // Esconde a grade de botões
    document.getElementById('grid-servicos').classList.add('hidden');
    
    // Preenche os dados da senha
    document.getElementById('display-senha').textContent = codigo;
    document.getElementById('info-servico').textContent = `SERVIÇO: ${tipo}`;
    
    // Mostra o bloco de sucesso
    const feedback = document.getElementById('feedback-sucesso');
    feedback.classList.remove('hidden');

    // Após 5 segundos, volta para a tela inicial automaticamente
    setTimeout(() => {
        feedback.classList.add('hidden');
        document.getElementById('grid-servicos').classList.remove('hidden');
    }, 5000);
}