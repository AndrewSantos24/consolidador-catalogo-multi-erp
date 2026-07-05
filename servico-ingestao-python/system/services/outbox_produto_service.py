from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from system.schemas.produto_schema import ProdutoNormalizado
from system.repositories.outbox_produto_repository import salvar_outbox_produto


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