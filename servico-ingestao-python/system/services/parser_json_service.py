from system.constants.campos_erp_json import CamposErpJson
from system.schemas.produto_schema import ProdutoNormalizado


def converter_item_json_para_produto(item: dict) -> ProdutoNormalizado:
    """Converte um item JSON do ERP para ProdutoNormalizado.

    :param dict item: Item do payload JSON enviado pelo ERP
    :return: Produto no formato padrão da aplicação
    """

    return ProdutoNormalizado(
        id=str(item[CamposErpJson.CODIGO_PRODUTO]).strip(),
        sku=str(item[CamposErpJson.SKU]).strip(),
        nome=str(item[CamposErpJson.DESCRICAO]).strip(),
        preco_lista=float(item[CamposErpJson.PRECO_LISTA]),
        preco_desconto=float(item[CamposErpJson.PRECO_DESCONTO]),
        categoria=str(item[CamposErpJson.DEPARTAMENTO]).strip(),
        atualizado_em=item[CamposErpJson.ATUALIZADO_EM],
    )


def normalizar_produtos_json(payload: dict) -> list[ProdutoNormalizado]:
    """Normaliza uma lista de produtos recebida via payload JSON.

    :param dict payload: Payload JSON enviado pelo ERP
    :return: Lista de produtos normalizados
    """

    produtos = payload.get(CamposErpJson.ITENS, [])

    return [
        converter_item_json_para_produto(item)
        for item in produtos
    ]