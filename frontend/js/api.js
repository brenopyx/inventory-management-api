export async function login(email, senha) {
    const response = await fetch("http://localhost:8000/usuarios/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, senha })
    });
    if (!response.ok) {
        throw new Error("Email ou senha incorretos");
    }
    return await response.json();
}
export async function listarProdutos() {
    const response = await fetch("http://localhost:8000/produtos/", {
        method: "GET"
    });
    if (!response.ok) {
        throw new Error("Erro ao buscar produtos");
    }
    return await response.json();
}
export async function criarProduto(produto, token) {
    const response = await fetch("http://localhost:8000/produtos/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(produto)
    });
    if (!response.ok) {
        throw new Error("Erro ao criar produto");
    }
    return await response.json();
}
export async function listarCategorias() {
    const response = await fetch("http://localhost:8000/categorias/", {
        method: "GET"
    });
    if (!response.ok) {
        throw new Error("Erro ao buscar categorias");
    }
    return await response.json();
}
export async function criarCategoria(nome, token) {
    const response = await fetch("http://localhost:8000/categorias/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ nome })
    });
    if (!response.ok) {
        throw new Error("Erro ao criar categoria");
    }
    return await response.json();
}
export async function editarCategoria(id, nome, token) {
    const response = await fetch(`http://localhost:8000/categorias/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ nome })
    });
    if (!response.ok) {
        throw new Error("Erro ao editar categoria");
    }
    return await response.json();
}
export async function deletarCategoria(id, token) {
    const response = await fetch(`http://localhost:8000/categorias/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    if (!response.ok) {
        throw new Error("Erro ao excluir categoria");
    }
}
export async function editarProduto(id, produto, token) {
    const response = await fetch(`http://localhost:8000/produtos/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(produto)
    });
    if (!response.ok) {
        throw new Error("Erro ao editar produto");
    }
    return await response.json();
}
export async function deletarProduto(id, token) {
    const response = await fetch(`http://localhost:8000/produtos/${id}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    if (!response.ok) {
        throw new Error("Erro ao excluir produto");
    }
}
export async function listarMovimentacoes(produtoId) {
    const url = produtoId
        ? `http://localhost:8000/movimentacoes/?produto_id=${produtoId}`
        : "http://localhost:8000/movimentacoes/";
    const response = await fetch(url, {
        method: "GET"
    });
    if (!response.ok) {
        throw new Error("Erro ao buscar movimentações");
    }
    return await response.json();
}
export async function criarMovimentacao(movimentacao, token) {
    const response = await fetch("http://localhost:8000/movimentacoes/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(movimentacao)
    });
    if (!response.ok) {
        throw new Error("Erro ao criar movimentacao");
    }
    return await response.json();
}
export async function consultarEstoque(produtoId) {
    const response = await fetch(`http://localhost:8000/produtos/${produtoId}/estoque`, {
        method: "GET"
    });
    if (!response.ok) {
        throw new Error("Erro ao consultar estoque");
    }
    return await response.json();
}
