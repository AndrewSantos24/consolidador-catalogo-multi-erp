from schemas.produto_schema import ProdutoNormalizado


def converter_item_json_para_produto(item: dict) -> ProdutoNormalizado:
    """Converte um item JSON do ERP para ProdutoNormalizado.

    :param dict item: Item do payload JSON enviado pelo ERP
    :return: Produto no formato padrão da aplicação
    """

    return ProdutoNormalizado(
        id=str(item["productCode"]).strip(),
        sku=str(item["skuCode"]).strip(),
        nome=str(item["description"]).strip(),
        preco_lista=float(item["value"]),
        preco_desconto=float(item["discountValue"]),
        categoria=str(item["department"]).strip(),
        atualizado_em=item["updated_at"],
    )


def normalizar_produtos_json(payload: dict) -> list[ProdutoNormalizado]:
    """Normaliza uma lista de produtos recebida via payload JSON.

    :param dict payload: Payload JSON enviado pelo ERP
    :return: Lista de produtos normalizados
    """

    produtos = payload.get("items", [])

    return [
        converter_item_json_para_produto(item)
        for item in produtos
    ]