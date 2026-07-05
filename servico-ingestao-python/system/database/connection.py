from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from system.core.config import configuracoes


engine = create_engine(
    configuracoes.database_url,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def obter_sessao() -> Generator[Session, None, None]:
    """Obtém uma sessão do banco de dados.

    :return: Sessão ativa do SQLAlchemy
    """

    sessao = SessionLocal()

    try:
        yield sessao

    finally:
        sessao.close()