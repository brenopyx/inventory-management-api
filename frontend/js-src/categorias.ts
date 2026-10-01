import { listarCategorias, criarCategoria, editarCategoria, deletarCategoria } from "./api.js";
import { obterToken } from "./auth.js";

let categoriaEmEdicaoId: number | null = null;

export async function carregarCategorias() {
  const tabela = document.getElementById("tabela-categorias");
  if (!tabela) return;

  tabela.innerHTML = "";

  const categorias = await listarCategorias();

  categorias.forEach((categoria: any) => {
    const linha = document.createElement("tr")
    linha.innerHTML = `
      <td>${categoria.nome}</td>
      <td class = "actions">
        <button class= "btn btn-outline btn-small btn-editar" data-id="${categoria.id}" data-nome="${categoria.nome}">Editar</button>
        <button class= "btn btn-danger btn-small btn-excluir" data-id="${categoria.id}">Excluir</button>
      </td>
    `;
    tabela.appendChild(linha);
  });

  document.querySelectorAll(".btn-editar").forEach((botao) => {
    botao.addEventListener("click", () => iniciarEdicao(botao as HTMLElement))
  });

  document.querySelectorAll(".btn-excluir").forEach((botao) => {
    botao.addEventListener("click", () => excluirCategoriaSelecionada(botao as HTMLElement))
  });
}

export async function enviarFormularioCategoria() {
  const campoNome = document.getElementById("category-name") as HTMLInputElement;
  const nome = campoNome.value;
  const token = obterToken();

  if (!token) {
    alert("Você precisa estar logado.");
    return;
  }

  try {
    if (categoriaEmEdicaoId !== null) {
      await editarCategoria(categoriaEmEdicaoId, nome, token);
      categoriaEmEdicaoId = null;
    } else {
      await criarCategoria(nome, token);
    }
    campoNome.value = "";
    carregarCategorias();
  } catch (erro) {
    alert("Erro ao salvar categoria")
  }
}

const form = document.getElementById('category-form') as HTMLFormElement;
form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  await enviarFormularioCategoria();
});

carregarCategorias();


export async function iniciarEdicao(botao: HTMLElement) {
  const id = Number(botao.dataset.id);
  const nome = botao.dataset.nome ?? "";

  categoriaEmEdicaoId = id;
  (document.getElementById("category-name") as HTMLInputElement).value = nome;
}

export async function excluirCategoriaSelecionada(botao: HTMLElement) {
  const id = Number(botao.dataset.id);
  const token = obterToken();

  if (!token) {
    alert("Você precisa estar logado.");
    return;
  }

  if (!confirm("Tem certeza que deseja excluir essa categoria?"))
    return;

  try {
    await deletarCategoria(id, token);
    carregarCategorias();
  } catch (erro) {
    alert("Erro ao excluir. Verifique se não há produtos vinculados.");
  }
}
