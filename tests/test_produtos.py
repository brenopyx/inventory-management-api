def test_criar_produto(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]
    # POST PRODUTO
    response = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response.json()["id"]

    assert response.status_code == 200
    assert response.json()["nome"] == "Caneta"

def test_listar_produtos(client):
    #POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]
    #POST PRODUTO
    client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    client.post("/produtos/", json={"nome": "Borracha", "preco": 1.00, "categoria_id": categoria_id})

    response = client.get("/produtos/")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_buscar_produto(client):
    #POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]
    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    response = client.get(f"/produtos/{produto_id}")

    assert response.status_code == 200
    assert response.json()["nome"] == "Caneta"

def test_buscar_produto_inexistente(client):
    reponse = client.get("/produtos/999")

    assert reponse.status_code == 404

def test_atualiazar_produto(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]
    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    # PUT
    response = client.put(f"/produtos/{produto_id}", json={"nome": "Lapis", "preco": 1.5, "categoria_id": categoria_id})

    assert response.status_code == 200
    assert response.json()["nome"] == "Lapis"

def test_deletar_produto(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]
    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    # DELETE
    response = client.delete(f"/produtos/{produto_id}")

    assert response.status_code == 204

def test_deletar_produto_com_movimentacao(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]
    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]
    # POST MOVIMENTACAO
    response_movimentacao = client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "ENTRADA", "quantidade": 10})
    movimentacao_id = response_movimentacao.json()["id"]

    #DELETE
    response = client.delete(f"/produtos/{produto_id}")

    assert response.status_code == 400

def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/999")

    assert response.status_code == 404