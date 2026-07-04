from fastapi.encoders import jsonable_encoder

from system.schemas.produto_schema import ProdutoNormalizado
from system.services.parser_json_service import normalizar_produtos_json
from system.services.parser_txt_service import normalizar_produtos_txt
from system.services.parser_xml_service import normalizar_produtos_xml


def montar_resposta_ingestao(
    produtos: list[ProdutoNormalizado],
    origem: str,
) -> dict:
    """Monta a resposta padrão após normalizar produtos.

    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :param str origem: Origem/formato dos produtos recebidos
    :return: Resposta padrão da ingestão
    """

    return {
        "mensagem": f"Produtos {origem} normalizados com sucesso.",
        "origem": origem,
        "quantidade": len(produtos),
        "produtos": jsonable_encoder(produtos),
    }


def processar_ingestao_json(payload: dict) -> dict:
    """Processa uma carga de produtos recebida em JSON.

    :param dict payload: Payload JSON enviado pelo ERP
    :return: Resposta padrão com produtos normalizados
    """

    produtos = normalizar_produtos_json(payload)

    return montar_resposta_ingestao(
        produtos=produtos,
        origem="JSON",
    )


def processar_ingestao_xml(payload_xml: str) -> dict:
    """Processa uma carga de produtos recebida em XML.

    :param str payload_xml: Payload XML enviado pelo ERP
    :return: Resposta padrão com produtos normalizados
    """

    produtos = normalizar_produtos_xml(payload_xml)

    return montar_resposta_ingestao(
        produtos=produtos,
        origem="XML",
    )


def processar_ingestao_txt(payload_txt: str) -> dict:
    """Processa uma carga de produtos recebida em TXT.

    :param str payload_txt: Payload TXT enviado pelo ERP
    :return: Resposta padrão com produtos normalizados
    """

    produtos = normalizar_produtos_txt(payload_txt)

    return montar_resposta_ingestao(
        produtos=produtos,
        origem="TXT",
    )