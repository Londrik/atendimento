// Variáveis globais para os gráficos (permitir atualização)
let chartBarras = null;
let chartPizza = null;

async function carregarDados() {
    try {
        const response = await fetch('/api/v1/metrics');
        const data = await response.json();

        // 1. Atualizar os Cards de Resumo
        document.getElementById('card-total').textContent = data.resumo.total;
        document.getElementById('card-media').innerHTML = `${data.resumo.media_espera} <span class="text-lg font-light">min</span>`;

        // 2. Renderizar Gráfico de Barras (Volume por Hora)
        renderizarGraficoBarras(data.grafico_hora);

        // 3. Renderizar Gráfico de Pizza (Distribuição por Tipo)
        renderizarGraficoPizza(data.resumo.distribuicao);

    } catch (error) {
        console.error("Erro ao carregar métricas:", error);
    }
}

function renderizarGraficoBarras(dadosHora) {
    const ctx = document.getElementById('graficoBarras').getContext('2d');
    
    // Se o gráfico já existir, destrói para criar um novo (necessário para o Chart.js)
    if (chartBarras) chartBarras.destroy();

    chartBarras = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dadosHora.map(d => d.hora),
            datasets: [{
                label: 'Atendimentos',
                data: dadosHora.map(d => d.quantidade),
                backgroundColor: '#005DA5', // Azul SENAI
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
        }
    });
}

function renderizarGraficoPizza(distribuicao) {
    const ctx = document.getElementById('graficoPizza').getContext('2d');
    
    if (chartPizza) chartPizza.destroy();

    const labels = Object.keys(distribuicao);
    const valores = Object.values(distribuicao);

    chartPizza = new Chart(ctx, {
        type: 'doughnut', // Estilo rosca/pizza
        data: {
            labels: labels,
            datasets: [{
                data: valores,
                backgroundColor: ['#ef4444', '#22c55e', '#3b82f6'], // Cores: Vermelho, Verde, Azul
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

// Carrega os dados assim que a página abrir
window.onload = carregarDados;