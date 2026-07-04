from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def verificar_saude() -> dict[str, str]:
    """Verifica se o serviço está funcionando corretamente."""

    return {
        "status": "online",
        "servico": "servico-ingestao-python",
    }