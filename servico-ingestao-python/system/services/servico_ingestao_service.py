from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from system.core.config import configuracoes
from system.core.errors import AppError, RabbitMQError
from system.schemas.produto_schema import ProdutoNormalizado
from system.services.outbox_produto_service import salvar_produtos_pendentes_no_outbox
from system.services.parser_json_service import normalizar_produtos_json
from system.services.parser_txt_service import normalizar_produtos_txt
from system.services.parser_xml_service import normalizar_produtos_xml
from system.services.rabbitmq_publisher_service import publicar_produtos_rbmq



def montar_resposta_ingestao_publicada(
    produtos: list[ProdutoNormalizado],
    origem: str,
    quantidade_publicada: int,
) -> dict:
    """Monta a resposta padrão para produtos publicados na fila.

    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :param str origem: Origem/formato dos produtos recebidos
    :param int quantidade_publicada: Quantidade de produtos publicados na fila
    :return: Resposta padrão da ingestão publicada
    """

    return {
        "mensagem": f"Produtos {origem} processados e publicados com sucesso.",
        "status": "PUBLICADO",
        "origem": origem,
        "quantidade_normalizada": len(produtos),
        "quantidade_publicada": quantidade_publicada,
        "quantidade_pendente": 0,
        "fila": configuracoes.rabbitmq_fila_produtos,
        "produtos": jsonable_encoder(produtos),
    }

def montar_resposta_ingestao_pendente(
    produtos: list[ProdutoNormalizado],
    origem: str,
    quantidade_pendente: int,
    erro: str,
) -> dict:
    """Monta a resposta padrão para produtos salvos como pendentes.

    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :param str origem: Origem/formato dos produtos recebidos
    :param int quantidade_pendente: Quantidade de produtos salvos no outbox
    :param str erro: Mensagem do erro ocorrido na publicação
    :return: Resposta padrão da ingestão pendente
    """

    return {
        "mensagem": (
            f"Produtos {origem} normalizados, mas não publicados. "
            "Eles foram salvos para reprocessamento."
        ),
        "status": "PENDENTE_REPROCESSAMENTO",
        "origem": origem,
        "quantidade_normalizada": len(produtos),
        "quantidade_publicada": 0,
        "quantidade_pendente": quantidade_pendente,
        "fila": configuracoes.rabbitmq_fila_produtos,
        "erro": erro,
        "produtos": jsonable_encoder(produtos),
    }


def processar_produtos_normalizados(
    sessao: Session,
    produtos: list[ProdutoNormalizado],
    origem: str,
) -> dict:
    """Processa produtos normalizados publicando na fila ou salvando no outbox.

    :param Session sessao: Sessão ativa do banco de dados
    :param list[ProdutoNormalizado] produtos: Lista de produtos normalizados
    :param str origem: Origem/formato dos produtos recebidos
    :return: Resposta padrão do processamento
    """

    try:
        quantidade_publicada = publicar_produtos_rbmq(produtos)

        return montar_resposta_ingestao_publicada(
            produtos=produtos,
            origem=origem,
            quantidade_publicada=quantidade_publicada,
        )

    except RabbitMQError as erro:
        quantidade_pendente = salvar_produtos_pendentes_no_outbox(
            sessao=sessao,
            produtos=produtos,
            origem=origem,
            erro=erro.mensagem,
        )

        return montar_resposta_ingestao_pendente(
            produtos=produtos,
            origem=origem,
            quantidade_pendente=quantidade_pendente,
            erro=erro.mensagem,
        )


def processar_ingestao_json(payload: dict, sessao: Session) -> dict:
    """Processa uma carga de produtos recebida em JSON.

    :param dict payload: Payload JSON enviado pelo ERP
    :param Session sessao: Sessão ativa do banco de dados
    :return: Resposta padrão com produtos processados
    """

    try:
        produtos = normalizar_produtos_json(payload)

    except Exception as erro:
        raise AppError(
            mensagem=f"Payload JSON inválido: {erro}",
            status_code=400,
        ) from erro

    return processar_produtos_normalizados(
        sessao=sessao,
        produtos=produtos,
        origem="JSON",
    )


def processar_ingestao_xml(payload_xml: str, sessao: Session) -> dict:
    """Processa uma carga de produtos recebida em XML.

    :param str payload_xml: Payload XML enviado pelo ERP
    :param Session sessao: Sessão ativa do banco de dados
    :return: Resposta padrão com produtos processados
    """

    try:
        produtos = normalizar_produtos_xml(payload_xml)

    except Exception as erro:
        raise AppError(
            mensagem=f"Payload XML inválido: {erro}",
            status_code=400,
        ) from erro

    return processar_produtos_normalizados(
        sessao=sessao,
        produtos=produtos,
        origem="XML",
    )


def processar_ingestao_txt(payload_txt: str, sessao: Session) -> dict:
    """Processa uma carga de produtos recebida em TXT.

    :param str payload_txt: Payload TXT enviado pelo ERP
    :param Session sessao: Sessão ativa do banco de dados
    :return: Resposta padrão com produtos processados
    """

    try:
        produtos = normalizar_produtos_txt(payload_txt)

    except Exception as erro:
        raise AppError(
            mensagem=f"Payload TXT inválido: {erro}",
            status_code=400,
        ) from erro

    return processar_produtos_normalizados(
        sessao=sessao,
        produtos=produtos,
        origem="TXT",
    )