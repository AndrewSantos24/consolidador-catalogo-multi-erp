from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from system.api.v1.routes.health_routes import router as health_router
from system.api.v1.routes.ingestao_routes import router as ingestao_router
from system.api.v1.routes.reprocessamento_routes import router as reprocessamento_router
from system.core.config import configuracoes
from system.database.inicializador import inicializar_banco

@asynccontextmanager
async def gerenciar_criacao_tabela(app: FastAPI) -> AsyncGenerator[None, None]:
    """Executa ações ao iniciar e finalizar a aplicação.

    :param FastAPI app: Aplicação FastAPI
    :return: Controle do ciclo de vida da aplicação
    """

    inicializar_banco()

    yield


app = FastAPI(
    title=configuracoes.nome_aplicacao,
    version="0.1.0",
    lifespan=gerenciar_criacao_tabela
)


app.include_router(health_router, prefix="/api/v1")
app.include_router(ingestao_router, prefix="/api/v1")
app.include_router(reprocessamento_router, prefix="/api/v1")