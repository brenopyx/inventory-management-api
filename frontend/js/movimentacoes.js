import { listarMovimentacoes, criarMovimentacao, listarProdutos } from "./api.js";
import { obterToken } from "./auth.js";
import { formatData } from "./date.js";
export async function carregarMovimentacoes(produtoId) {
    const tabela = document.getElementById("tabela-movimentacoes");
    if (!tabela)
        return;
    tabela.innerHTML = "";
    const movimentacoes = await listarMovimentacoes(produtoId);
    movimentacoes.forEach((mov) => {
        const linha = document.createElement("tr");
        linha.innerHTML = `
      <td>${mov.produto_id}</td>
      <td>${mov.tipo}</td>
      <td>${mov.quantidade} un.</td>
      <td>${mov.motivo ?? ""}</td>
      <td>${formatData(mov.criado_em)}</td>
    `;
        tabela.appendChild(linha);
    });
}
export async function carregarProdutosParaSelect() {
    const selectFormulario = document.getElementById("movement-product");
    const selectFiltro = document.getElementById("history-product");
    if (!selectFormulario || !selectFiltro)
        return;
    const produtos = await listarProdutos();
    produtos.forEach((produto) => {
        const opcaoFormulario = document.createElement("option");
        opcaoFormulario.value = produto.id;
        opcaoFormulario.textContent = produto.nome;
        selectFormulario.appendChild(opcaoFormulario);
        const opcaoFiltro = document.createElement("option");
        opcaoFiltro.value = produto.id;
        opcaoFiltro.textContent = produto.nome;
        selectFiltro.appendChild(opcaoFiltro);
    });
}
export async function enviarFormularioMovimentacao() {
    const campoProduto = document.getElementById("movement-product");
    const campoTipo = document.getElementById("movement-type");
    const campoQuantidade = document.getElementById("movement-quantity");
    const campoMotivo = document.getElementById("movement-reason");
    const token = obterToken();
    if (!token) {
        alert("Você precisa estar logado.");
        return;
    }
    const movimentacao = {
        produto_id: parseInt(campoProduto.value),
        tipo: campoTipo.value,
        quantidade: parseInt(campoQuantidade.value),
        motivo: campoMotivo.value || null
    };
    try {
        await criarMovimentacao(movimentacao, token);
        campoProduto.value = "";
        campoTipo.value = "";
        campoQuantidade.value = "";
        campoMotivo.value = "";
        carregarMovimentacoes();
    }
    catch (erro) {
        alert("Erro ao registrar movimentação. Verifique o estoque disponivel.");
    }
}
export async function filtrarMovimentacoesPorProduto() {
    const selectFiltro = document.getElementById("history-product");
    const produtoId = selectFiltro.value ? parseInt(selectFiltro.value) : undefined;
    carregarMovimentacoes(produtoId);
}
const form = document.getElementById("movement-form");
form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    await enviarFormularioMovimentacao();
});
const botaoFiltrar = document.getElementById("btn-filtrar");
botaoFiltrar.addEventListener("click", filtrarMovimentacoesPorProduto);
carregarProdutosParaSelect();
carregarMovimentacoes();
