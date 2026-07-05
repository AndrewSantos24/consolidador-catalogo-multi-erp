from sqlalchemy.orm import Session

from system.models.outbox_produto_model import OutboxProduto


def salvar_outbox_produto(
    sessao: Session,
    origem: str,
    payload: dict,
    erro: str | None = None,
) -> OutboxProduto:
    """Salva uma mensagem de produto pendente no outbox.

    :param Session sessao: Sessão ativa do banco de dados
    :param str origem: Origem do payload recebido, como JSON, XML ou TXT
    :param dict payload: Produto normalizado que será salvo como JSON
    :param str | None erro: Mensagem de erro que motivou o registro no outbox
    :return: Registro salvo na tabela outbox_produtos
    """

    registro = OutboxProduto(
        origem=origem,
        payload=payload,
        status="PENDENTE",
        tentativas=0,
        erro=erro,
    )

    sessao.add(registro)
    sessao.commit()
    sessao.refresh(registro)

    return registro


def listar_outbox_produtos_pendentes(
    sessao: Session,
    limite: int = 100,
) -> list[OutboxProduto]:
    """Lista mensagens pendentes do outbox.

    :param Session sessao: Sessão ativa do banco de dados
    :param int limite: Quantidade máxima de registros retornados
    :return: Lista de registros pendentes
    """

    return (
        sessao.query(OutboxProduto)
        .filter(OutboxProduto.status == "PENDENTE")
        .order_by(OutboxProduto.criado_em.asc())
        .limit(limite)
        .all()
    )