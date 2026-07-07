from system.database.base import Base
from system.database.connection import engine
from system.models import OutboxProduto


def inicializar_banco() -> None:
    """Inicializa as tabelas do banco de dados da aplicação."""

    _ = OutboxProduto

    Base.metadata.create_all(bind=engine)