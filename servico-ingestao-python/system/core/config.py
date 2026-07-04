from pydantic_settings import BaseSettings


class Configuracoes(BaseSettings):
    """Representa as configurações principais da aplicação."""

    nome_aplicacao: str = "Serviço de Ingestão - Catálogo Multi-ERP"
    ambiente: str = "desenvolvimento"


configuracoes = Configuracoes()