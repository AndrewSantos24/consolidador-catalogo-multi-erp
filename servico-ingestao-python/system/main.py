from fastapi import FastAPI

from system.api.v1.routes.health_routes import router as health_router
from system.api.v1.routes.ingestao_routes import router as ingestao_router
from system.core.config import configuracoes


app = FastAPI(
    title=configuracoes.nome_aplicacao,
    version="0.1.0",
)


app.include_router(health_router, prefix="/api/v1")
app.include_router(ingestao_router, prefix="/api/v1")