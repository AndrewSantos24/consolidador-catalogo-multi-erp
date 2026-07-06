from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from system.core.errors import RabbitMQError
from system.schemas.produto_schema import ProdutoNormalizado
from system.repositories.outbox_produto_repository import (
    listar_outbox_produtos_pendentes,
    marcar_outbox_produto_como_erro,
    marcar_outbox_produto_como_publicado,
    salvar_outbox_produto,
)
from system.schemas.produto_schema import ProdutoNormalizado
from system.services.rabbitmq_publisher_service import publicar_produtos_rbmq

def salvar_produto_pendente_no_outbox(
    sessao: Session,
    produto: ProdutoNormalizado,
    origem: str,
    erro: str | None = None,
) -> None:
    """Salva um produto normalizado como pendente no outbox.

    :param Session sessao: Sessão ativa do banco de dados
    :param ProdutoNormalizado produto: Produto normalizado que será salvo
    :param str origem: Origem do produto recebido, como JSON, XML ou TXT
    :param str | None erro: Mensagem de erro que motivou o registro
    """

    payload = jsonable_encoder(produto)

    salvar_outbox_produto(
        sessao=sessao,
        origem=origem,
        payload=payload,
        erro=erro,
    )

def salvar_produtos_pendentes_no_outbox(
    sessao: Session,
    produtos: list[ProdutoNormalizado],
    origem: str,
    erro: str | None = None,
) -> int:
    """Salva uma lista de produtos normalizados como pendente no outbox.

    :param Session sessao: Sessão ativa do banco de dados
    :param list[ProdutoNormalizado] produtos: Produtos normalizados que serão salvos
    :param str origem: Origem dos produtos recebidos, como JSON, XML ou TXT
    :param str | None erro: Mensagem de erro que motivou o registro
    :return: Quantidade de produtos salvos no outbox
    """

    for produto in produtos:
        salvar_produto_pendente_no_outbox(
            sessao=sessao,
            produto=produto,
            origem=origem,
            erro=erro,
        )

    return len(produtos)

def converter_payload_outbox_para_produto(payload: dict) -> ProdutoNormalizado:
    """Converte o payload salvo no outbox para ProdutoNormalizado.

    :param dict payload: Payload salvo na tabela outbox_produtos
    :return: Produto normalizado
    """

    return ProdutoNormalizado(**payload)

def reprocessar_outbox_produtos(
    sessao: Session,
    limite: int = 100,
) -> dict:
    """Reprocessa produtos pendentes no outbox.

    :param Session sessao: Sessão ativa do banco de dados
    :param int limite: Quantidade máxima de registros reprocessados
    :return: Resumo do reprocessamento
    """

    registros = listar_outbox_produtos_pendentes(
        sessao=sessao,
        limite=limite,
    )

    total_pendentes = len(registros)
    total_publicados = 0
    total_com_erro = 0

    for registro in registros:
        try:
            produto = converter_payload_outbox_para_produto(registro.payload)

            publicar_produtos_rbmq([produto])

            marcar_outbox_produto_como_publicado(
                sessao=sessao,
                registro=registro,
            )

            total_publicados += 1

        except RabbitMQError as erro:
            marcar_outbox_produto_como_erro(
                sessao=sessao,
                registro=registro,
                erro=erro.mensagem,
            )

            total_com_erro += 1

    return {
        "mensagem": "Reprocessamento do outbox executado.",
        "total_pendentes_encontrados": total_pendentes,
        "total_publicados": total_publicados,
        "total_com_erro": total_com_erro,
    }