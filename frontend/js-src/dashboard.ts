import { listarProdutos, consultarEstoque, listarCategorias } from "./api.js";

const LIMITE_ESTOQUE_BAIXO = 10;

export async function carregarDashboard() {
  const tabela = document.getElementById("tabela-produtos");
  if (!tabela) return;

  const produtos = await listarProdutos();
  const categorias = await listarCategorias(); // Total de categorias

  let produtosEstoqueBaixo = 0;
  
  for (const produto of produtos) {
    const estoque = await consultarEstoque(produto.id)
    const linha = document.createElement("tr");

    if (estoque.estoque_atual < LIMITE_ESTOQUE_BAIXO) {
      produtosEstoqueBaixo++;
      linha.classList.add("low-stock");
    }

    linha.innerHTML = `
      <td>${produto.nome}</td>
      <td>${produto.categoria.nome}</td>
      <td>R$ ${produto.preco.toFixed(2)}</td>
      <td>${estoque.estoque_atual} un.</td>
    `;
    tabela.appendChild(linha);
  };
  atualizarMetricas("metric-produtos", produtos.length);
  atualizarMetricas("metric-categorias", categorias.length);
  atualizarMetricas("metric-estoque-baixo", produtosEstoqueBaixo);

}
carregarDashboard()


export async function atualizarMetricas(id: string, valor: number) {
  const elemento = document.getElementById(id);
  if (elemento) elemento.textContent = String(valor);
}
