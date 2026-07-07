import xml.etree.ElementTree as ET

from system.constants.campos_erp_xml import CamposErpXml
from system.schemas.produto_schema import ProdutoNormalizado


def converter_item_xml_para_produto(elemento: ET.Element) -> ProdutoNormalizado:
    """Converte um item XML do ERP para ProdutoNormalizado.

    :param ET.Element elemento: Elemento XML de um produto
    :return: Produto no formato padrão da aplicação
    """

    return ProdutoNormalizado(
        id=str(elemento.findtext(CamposErpXml.ID, "")).strip(),
        sku=str(elemento.findtext(CamposErpXml.SKU, "")).strip(),
        nome=str(elemento.findtext(CamposErpXml.NOME, "")).strip(),
        preco_lista=float(elemento.findtext(CamposErpXml.PRECO_LISTA, "0")),
        preco_desconto=float(elemento.findtext(CamposErpXml.PRECO_DESCONTO, "0")),
        categoria=str(elemento.findtext(CamposErpXml.CATEGORIA, "")).strip(),
        atualizado_em=str(elemento.findtext(CamposErpXml.ATUALIZADO_EM, "")).strip(),
    )


def normalizar_produtos_xml(payload_xml: str) -> list[ProdutoNormalizado]:
    """Normaliza uma lista de produtos recebida via payload XML.

    :param str payload_xml: Payload XML enviado pelo ERP
    :return: Lista de produtos normalizados
    """

    raiz = ET.fromstring(payload_xml)
    produtos = raiz.findall(CamposErpXml.PRODUTO)

    return [
        converter_item_xml_para_produto(produto)
        for produto in produtos
    ]