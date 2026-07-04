import xml.etree.ElementTree as ET

from system.schemas.produto_schema import ProdutoNormalizado


def converter_item_xml_para_produto(elemento: ET.Element) -> ProdutoNormalizado:
    """Converte um item XML do ERP para ProdutoNormalizado.

    :param ET.Element elemento: Elemento XML de um produto
    :return: Produto no formato padrão da aplicação
    """

    return ProdutoNormalizado(
        id=str(elemento.findtext("id", "")).strip(),
        sku=str(elemento.findtext("sku", "")).strip(),
        nome=str(elemento.findtext("name", "")).strip(),
        preco_lista=float(elemento.findtext("price/list", "0")),
        preco_desconto=float(elemento.findtext("price/discount", "0")),
        categoria=str(elemento.findtext("category", "")).strip(),
        atualizado_em=str(elemento.findtext("lastUpdate", "")).strip(),
    )


def normalizar_produtos_xml(payload_xml: str) -> list[ProdutoNormalizado]:
    """Normaliza uma lista de produtos recebida via payload XML.

    :param str payload_xml: Payload XML enviado pelo ERP
    :return: Lista de produtos normalizados
    """

    raiz = ET.fromstring(payload_xml)
    produtos = raiz.findall("product")

    return [
        converter_item_xml_para_produto(produto)
        for produto in produtos
    ]