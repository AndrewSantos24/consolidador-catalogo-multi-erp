from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from system.database.connection import obter_sessao
from system.services.outbox_produto_service import reprocessar_outbox_produtos


router = APIRouter(prefix="/reprocessamento", tags=["Reprocessamento"])


@router.post("/outbox-produtos")
def reprocessar_produtos_pendentes(
    limite: int = Query(default=100, ge=1, le=500),
    sessao: Session = Depends(obter_sessao),
) -> dict:
    """Reprocessa produtos pendentes salvos no outbox.

    Exemplo de chamada:

    POST /api/v1/reprocessamento/outbox-produtos?limite=100

    :param int limite: Quantidade máxima de registros pendentes reprocessados
    :param Session sessao: Sessão ativa do banco de dados
    :return: Resumo do reprocessamento
    """

    return reprocessar_outbox_produtos(
        sessao=sessao,
        limite=limite,
    )