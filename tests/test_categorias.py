def test_criar_categoria(client):
    response = client.post("/categorias/", json={"nome": "Papelaria"})

    assert response.status_code == 200
    assert response.json()["nome"] == "Papelaria"

def test_listar_categorias(client):
    # POST
    client.post("/categorias/", json={"nome": "Papelaria"})
    client.post("/categorias/", json={"nome": "Limpeza"})

    # GET
    response = client.get("/categorias/")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_buscar_categoria(client):
    # POST
    response_criação = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_criação.json()["id"]

    # GET
    response = client.get(f"/categorias/{categoria_id}")

    assert response.status_code == 200
    assert response.json()["nome"] == "Papelaria"

def test_buscar_categoria_inexistente(client):
    reponse = client.get("/categorias/999")

    assert reponse.status_code == 404

def test_atualizar_categoria(client):
    # POST
    response_criação = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_criação.json()["id"]

    # PUT
    response = client.put(f"/categorias/{categoria_id}", json={"nome": "Papelaria e Tesouraria"})

    assert response.status_code == 200
    assert response.json()["nome"] == "Papelaria e Tesouraria"

def test_deletar_categoria_sem_produtos(client):
    # POST
    response_criação = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_criação.json()["id"]

    # DELETE
    response = client.delete(f"/categorias/{categoria_id}")

    assert response.status_code == 204

def test_deletar_categoria_com_produtos_vinculados(client):
    # POST
    response_categoria = client.post("/categorias/", json={"nome": "Papelaria"})
    categoria_id = response_categoria.json()["id"]
    response_produto = client.post("/produtos/", json={"nome": "Caneta", "preco": 2.5, "categoria_id": categoria_id})
    produto_id = response_produto.json()["id"]

    # DELETE
    response = client.delete(f"/categorias/{categoria_id}")

    assert response.status_code == 400

def test_deletar_categoria_inexistente(client):
    response = client.delete("/categorias/999")

    assert response.status_code == 404

