import { listarProdutos, criarProduto, listarCategorias, deletarProduto, editarProduto } from "./api.js";
import { obterToken } from "./auth.js";

let produtoEmEdicao: number | null = null;

export async function carregarProdutos() {
  const tabela = document.getElementById("tabela-produtos-lista");
  if (!tabela) return;

  tabela.innerHTML = ""

  const produtos = await listarProdutos();

  produtos.forEach((produto: any) => {
    const linha = document.createElement("tr");
    linha.innerHTML = `
      <td>${produto.nome}</td>
      <td>R$ ${produto.preco.toFixed(2)}</td>
      <td>${produto.categoria.nome}</td>
      <td>${produto.descricao ?? ""}</td>
      <td class = "actions">
        <button class="btn btn-outline btn-small btn-editar" data-id="${produto.id}" data-nome="${produto.nome}">Editar</button>
        <button class="btn btn-danger btn-small btn-excluir" data-id="${produto.id}">Excluir</button>
      </td>
    `;
    tabela.appendChild(linha)
  });

  document.querySelectorAll(".btn-editar").forEach((botao) => {
    botao.addEventListener("click", () => iniciarEdicao(botao as HTMLElement))
  });
  
  document.querySelectorAll(".btn-excluir").forEach((botao) => {
    botao.addEventListener("click", () => excluirProdutoSelecionado(botao as HTMLElement))
  });
}

export async function carregarOpcoesCategorias() {
  const select = document.getElementById("product-category") as HTMLSelectElement;
  if (!select) return;

  const categorias = await listarCategorias();

  categorias.forEach((categoria: any) => {
    const opcao = document.createElement("option");
    opcao.value = categoria.id;
    opcao.textContent = categoria.nome;
    select.appendChild(opcao)
  });
}

export async function enviarFormularioProduto() {
  const campoNome = document.getElementById("product-name") as HTMLInputElement;
  const campoPreco = document.getElementById("product-price") as HTMLInputElement;
  const campoCategoria = document.getElementById("product-category") as HTMLSelectElement;
  const campoDescricao = document.getElementById("product-description") as HTMLTextAreaElement;
  const token = obterToken();

  if (!token) {
    alert("Você precisa estar logado.");
    return;
  }

  const produto = {
    nome: campoNome.value,
    preco: parseFloat(campoPreco.value),
    categoria_id: parseInt(campoCategoria.value),
    descricao: campoDescricao.value || null
  }

  try {
    if (produtoEmEdicao !== null) {
      await editarProduto(produtoEmEdicao, produto, token);
      produtoEmEdicao = null;
    } else {
      await criarProduto(produto, token);
    }
    campoNome.value = ""
    campoPreco.value = ""
    campoCategoria.value = ""
    campoDescricao.value = ""
    carregarProdutos();
  } catch (erro) {
    alert("Erro ao criar Produto")
  }
}


export async function iniciarEdicao(botao: HTMLElement) {
  const id = Number(botao.dataset.id);
  const nome = botao.dataset.nome ?? "";

  produtoEmEdicao = id;
  (document.getElementById("product-name") as HTMLInputElement).value = nome;
}

export async function excluirProdutoSelecionado(botao: HTMLElement) {
  const id = Number(botao.dataset.id);
  const token = obterToken();

  if (!token) {
    alert("Você precisa esta logado.");
    return;
  }

  if (!confirm("Tem certeza  que deseja excluir esse produto?"))
    return;

  try {
    await deletarProduto(id, token);
    carregarProdutos();
  } catch (erro) {
    alert("Erro ao excluir produto")
  }

}


const form = document.getElementById("product-form") as HTMLFormElement;

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  await enviarFormularioProduto();
})

carregarOpcoesCategorias();
carregarProdutos();