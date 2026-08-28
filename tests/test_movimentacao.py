def test_criar_movimentacao(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]

    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    #POST MOVIMENTACAO
    response = client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "ENTRADA", "quantidade": 10})
    movimentacao_id = response.json()["id"]

    assert response.status_code == 200
    assert response.json()["tipo"] == "ENTRADA"

def test_listar_movimentacoes(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]

    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    #POST MOVIMENTACAO
    client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "ENTRADA", "quantidade": 10})
    client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "SAIDA", "quantidade": 2})
    client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "ENTRADA", "quantidade": 5})

    # GET
    response = client.get("/movimentacoes/")

    assert response.status_code == 200
    assert len(response.json()) == 3

def test_buscar_movimentacao(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]

    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    #POST MOVIMENTACAO
    response_movimentacao = client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "ENTRADA", "quantidade": 10})
    movimentacao_id = response_movimentacao.json()["id"]  

    # GET
    response = client.get(f"/movimentacoes/{movimentacao_id}")

    assert response.status_code == 200
    assert response.json()["tipo"] == "ENTRADA"

def test_buscar_movimentacao_inexistente(client):
    response = client.get("/movimentacao/999")

    assert response.status_code == 404

def test_verificar_saida_valida(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]

    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    # POST MOVIMENTACAO ENTRADA
    response_movimentacao_entrada = client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "ENTRADA", "quantidade": 10})
    movimentacao_entrada_id = response_movimentacao_entrada.json()["id"]

    # POST MOVIMENTACAO SAIDA
    response_movimentacao_saida = client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "SAIDA", "quantidade": 5})
    movimentacao_saida_id = response_movimentacao_saida.json()["id"]

    assert response_movimentacao_saida.status_code == 200

def test_verificar_saida_maior_estoque(client):
    # POST CATEGORIA
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]

    # POST PRODUTO
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    # POST MOVIMENTACAO ENTRADA
    response_movimentacao_entrada = client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "ENTRADA", "quantidade": 10})
    movimentacao_entrada_id = response_movimentacao_entrada.json()["id"]
    
    # POST MOVIMENTACAO SAIDA
    response = client.post("/movimentacoes/", json={"produto_id": produto_id, "tipo": "SAIDA", "quantidade": 20})
    
    assert response.status_code == 400

def test_criar_movimentacao_produto_inexistente(client):
    #POST
    response = client.post("/movimentacoes/", json={"produto_id": 999 ,"tipo": "ENTRADA", "quantidade": 10})

    assert response.status_code == 404