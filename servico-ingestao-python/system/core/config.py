from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    """Representa as configurações principais da aplicação."""

    nome_aplicacao: str
    ambiente: str

    rabbitmq_host: str
    rabbitmq_porta: int
    rabbitmq_usuario: str
    rabbitmq_senha: str
    rabbitmq_fila_produtos: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


configuracoes = Configuracoes()