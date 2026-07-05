from fastapi.encoders import jsonable_encoder

from system.schemas.produto_schema import ProdutoNormalizado
from system.services.parser_json_service import normalizar_produtos_json
from system.services.parser_txt_service import normalizar_produtos_txt
from system.services.parser_xml_service import normalizar_produtos_xml
from system.services.rabbitmq_publisher_service import publicar_produtos_normalizados



def montar_resposta_ingestao(
    produtos: list[ProdutoNormalizado],
    origem: str,
    quantidade_publicada: int,
) -> dict:
    """Monta a resposta padrão após processar uma carga de produtos.

    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :param str origem: Origem/formato dos produtos recebidos
    :param int quantidade_publicada: Quantidade de produtos publicados na fila
    :return: Resposta padrão da ingestão
    """

    return {
        "mensagem": f"Produtos {origem} processados com sucesso.",
        "origem": origem,
        "quantidade_normalizada": len(produtos),
        "quantidade_publicada": quantidade_publicada,
        "fila": "catalogo.produtos.normalizados",
        "produtos": jsonable_encoder(produtos),
    }


def processar_ingestao_json(payload: dict) -> dict:
    """Processa uma carga de produtos recebida em JSON.

    :param dict payload: Payload JSON enviado pelo ERP
    :return: Resposta padrão com produtos normalizados e publicados
    """

    produtos = normalizar_produtos_json(payload)
    quantidade_publicada = publicar_produtos_normalizados(produtos)

    return montar_resposta_ingestao(
        produtos=produtos,
        origem="JSON",
        quantidade_publicada=quantidade_publicada
    )


def processar_ingestao_xml(payload_xml: str) -> dict:
    """Processa uma carga de produtos recebida em XML.

    :param str payload_xml: Payload XML enviado pelo ERP
    :return: Resposta padrão com produtos normalizados e publicados
    """

    produtos = normalizar_produtos_xml(payload_xml)
    quantidade_publicada = publicar_produtos_normalizados(produtos)

    return montar_resposta_ingestao(
        produtos=produtos,
        origem="XML",
        quantidade_publicada=quantidade_publicada
    )


def processar_ingestao_txt(payload_txt: str) -> dict:
    """Processa uma carga de produtos recebida em TXT.

    :param str payload_txt: Payload TXT enviado pelo ERP
    :return: Resposta padrão com produtos normalizados e publicados
    """

    produtos = normalizar_produtos_txt(payload_txt)
    quantidade_publicada = publicar_produtos_normalizados(produtos)

    return montar_resposta_ingestao(
        produtos=produtos,
        origem="TXT",
        quantidade_publicada=quantidade_publicada
    )